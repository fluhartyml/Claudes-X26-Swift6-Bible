//
//  VaultWebView.swift
//  Claudes X26 Swift6 Bible
//
//  Universal WKWebView wrapper that renders the currently-open document
//  in the vault. Intercepts link clicks: internal vault links route
//  back through VaultModel (keeping file-tree selection in sync); external
//  links open in the system browser.
//

import SwiftUI
import WebKit
import Combine

#if os(macOS)
import AppKit
typealias PlatformView = NSView
typealias PlatformViewRepresentable = NSViewRepresentable
#else
import UIKit
typealias PlatformView = UIView
typealias PlatformViewRepresentable = UIViewRepresentable
#endif

struct VaultWebView: PlatformViewRepresentable {
    let documentURL: URL?
    let vaultRoot: URL?
    let textScale: Double
    let onInternalNavigate: (URL) -> Void

    /// Shared bridge that holds a reference to the live WebView so the
    /// SwiftUI toolbar can trigger actions (Highlight) on it.
    final class Bridge: ObservableObject {
        weak var webView: WKWebView?
        func highlightSelection() {
            let js = """
            (function(){
              var sel = window.getSelection();
              if (!sel || sel.rangeCount === 0 || sel.toString().length === 0) return;
              var range = sel.getRangeAt(0);
              var mark = document.createElement('mark');
              mark.className = 'user-hl';
              try { range.surroundContents(mark); }
              catch (e) {
                // Selection spans multiple elements — fallback: extract+wrap.
                var frag = range.extractContents();
                mark.appendChild(frag);
                range.insertNode(mark);
              }
              sel.removeAllRanges();
              // Trigger our save path.
              document.body.dispatchEvent(new Event('input', { bubbles: true }));
            })();
            """
            webView?.evaluateJavaScript(js)
        }
    }

    // MARK: - Platform bridges

    #if os(macOS)
    func makeNSView(context: Context) -> WKWebView { makeWebView(context: context) }
    func updateNSView(_ webView: WKWebView, context: Context) {
        loadIfNeeded(webView)
        applyTextScale(webView)
    }
    #else
    func makeUIView(context: Context) -> WKWebView { makeWebView(context: context) }
    func updateUIView(_ webView: WKWebView, context: Context) {
        loadIfNeeded(webView)
        applyTextScale(webView)
    }
    #endif

    private func applyTextScale(_ webView: WKWebView) {
        let js = """
        (function(){
          var id='__claude-text-scale';
          var s=document.getElementById(id);
          if(!s){s=document.createElement('style');s.id=id;document.head.appendChild(s);}
          s.textContent='body{zoom:\(textScale);}';
        })();
        """
        webView.evaluateJavaScript(js)
    }

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    // MARK: - Shared

    @EnvironmentObject private var bridge: Bridge

    private func makeWebView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences.allowsContentJavaScript = true

        // Wire up the content-edit bridge so the reader can type / Scribble
        // anywhere on the page and we can persist the change.
        config.userContentController.add(context.coordinator, name: "pageEdit")
        config.userContentController.addUserScript(Self.editableScript)
        config.userContentController.addUserScript(Self.highlightStyleScript)

        // Serve vault content via a custom URL scheme so iOS's file://
        // sandbox-extension quirks in subdirectories stop biting us.
        let handler = VaultURLSchemeHandler { [vaultRoot] in vaultRoot }
        config.setURLSchemeHandler(handler, forURLScheme: VaultURLSchemeHandler.scheme)
        context.coordinator.schemeHandler = handler

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        bridge.webView = webView
        #if os(macOS)
        webView.setValue(false, forKey: "drawsBackground")
        #else
        webView.isOpaque = false
        webView.backgroundColor = .black
        webView.scrollView.backgroundColor = .black
        #endif
        return webView
    }

    /// Inject a minimal style for <mark class="user-hl"> so reader highlights
    /// render in amber on black without clashing with existing vault CSS.
    private static let highlightStyleScript: WKUserScript = {
        let source = """
        (function(){
          var s = document.createElement('style');
          s.textContent = 'mark.user-hl{background:#FFB000;color:#000;padding:0 0.1em;border-radius:2px;}';
          document.head.appendChild(s);
        })();
        """
        return WKUserScript(source: source, injectionTime: .atDocumentEnd, forMainFrameOnly: true)
    }()

    /// Script that runs at document end on every page load — makes body
    /// editable, enables spellcheck (lets Scribble work with Apple Pencil),
    /// and posts the updated HTML back to Swift when the user commits an
    /// edit (blur) or after a short debounce while typing.
    private static let editableScript: WKUserScript = {
        let source = """
        (function(){
          var body = document.body;
          if (!body) return;
          body.contentEditable = 'true';
          body.spellcheck = true;

          // In contentEditable, tapping a link normally puts the cursor
          // inside instead of navigating. Mark every <a> contentEditable=
          // 'false' so taps behave as ordinary link activations and
          // VaultWebView's WKNavigationDelegate picks them up. Re-run on
          // each DOM mutation so newly-inserted links are treated the
          // same way.
          function fixLinks(root){
            var links = (root || document).querySelectorAll('a');
            for (var i = 0; i < links.length; i++) {
              links[i].setAttribute('contenteditable', 'false');
              // Also mark navigation-style list items (<li> containing an <a>
              // with no block-level children like <p>, <ul>, <ol>) as
              // non-editable so taps in the bullet/padding area still
              // activate the link instead of popping the keyboard.
              var li = links[i].closest('li');
              if (li && !li.querySelector('p, ul, ol, h1, h2, h3, pre')) {
                li.setAttribute('contenteditable', 'false');
              }
            }
          }
          fixLinks(document);
          var mo = new MutationObserver(function(muts){
            for (var i = 0; i < muts.length; i++) {
              fixLinks(muts[i].target);
            }
          });
          mo.observe(body, { childList: true, subtree: true });

          // Capture-phase click handler: if the tap lands anywhere on (or
          // inside) an <a>, force navigation BEFORE contentEditable can
          // turn the tap into a cursor placement + keyboard reveal.
          document.addEventListener('click', function(e){
            var a = e.target.closest('a');
            if (a && a.href) {
              e.preventDefault();
              e.stopPropagation();
              window.location.href = a.href;
            }
          }, true);

          var timer = null;
          function send(){
            try {
              var html = document.documentElement.outerHTML;
              window.webkit.messageHandlers.pageEdit.postMessage(html);
            } catch (e) {}
          }
          body.addEventListener('input', function(){
            if (timer) clearTimeout(timer);
            timer = setTimeout(send, 1200);
          });
          body.addEventListener('blur', send, true);
        })();
        """
        return WKUserScript(source: source, injectionTime: .atDocumentEnd, forMainFrameOnly: true)
    }()

    private func loadIfNeeded(_ webView: WKWebView) {
        guard let url = documentURL, let root = vaultRoot else { return }
        guard let schemeURL = VaultURLSchemeHandler.url(for: url, root: root) else { return }
        // Only reload if the target URL differs from what's currently loaded.
        if webView.url == schemeURL { return }
        webView.load(URLRequest(url: schemeURL))
    }

    // MARK: - Coordinator — intercepts navigations

    final class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
        let parent: VaultWebView
        /// Retained so the WKWebViewConfiguration's handler reference stays alive.
        var schemeHandler: VaultURLSchemeHandler?
        init(_ parent: VaultWebView) { self.parent = parent }

        // Persist edits back to the document file in the vault.
        func userContentController(
            _ userContentController: WKUserContentController,
            didReceive message: WKScriptMessage
        ) {
            guard message.name == "pageEdit",
                  let html = message.body as? String,
                  let url = parent.documentURL else { return }
            do {
                try html.write(to: url, atomically: true, encoding: .utf8)
            } catch {
                // Best-effort save; ignore failures (e.g. bundle is read-only).
            }
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            parent.applyTextScale(webView)
            print("[wv] didFinish: \(webView.url?.lastPathComponent ?? "nil")")
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            print("[wv] didFail: \(error.localizedDescription)")
        }

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            print("[wv] didFailProvisionalNavigation: \(error.localizedDescription)")
        }

        func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
            print("[wv] didStart: \(webView.url?.lastPathComponent ?? "nil")")
        }

        func webView(
            _ webView: WKWebView,
            decidePolicyFor navigationAction: WKNavigationAction,
            decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
        ) {
            guard let url = navigationAction.request.url else {
                decisionHandler(.cancel)
                return
            }

            // Let initial loads and reloads through.
            if navigationAction.navigationType != .linkActivated {
                decisionHandler(.allow)
                return
            }

            // Internal vault link arrives as bible:// — route through VaultModel.
            if url.scheme == VaultURLSchemeHandler.scheme, let root = parent.vaultRoot {
                if let fileURL = VaultURLSchemeHandler.fileURL(for: url, root: root) {
                    decisionHandler(.cancel)
                    print("[tap] Link: \(fileURL.lastPathComponent)")
                    parent.onInternalNavigate(fileURL)
                    return
                }
            }

            // Legacy file:// links (if any survive in hand-authored HTML) —
            // resolve to vault-relative and bubble up.
            if url.isFileURL, let root = parent.vaultRoot {
                if url.path.hasPrefix(root.path) {
                    decisionHandler(.cancel)
                    print("[tap] Link: \(url.lastPathComponent)")
                    parent.onInternalNavigate(url)
                    return
                }
            }

            // External or cross-vault — hand off to the system.
            #if os(macOS)
            NSWorkspace.shared.open(url)
            #else
            UIApplication.shared.open(url)
            #endif
            decisionHandler(.cancel)
        }
    }
}
