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

    private func makeWebView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences.allowsContentJavaScript = true

        // Wire up the content-edit bridge so the reader can type / Scribble
        // anywhere on the page and we can persist the change.
        config.userContentController.add(context.coordinator, name: "pageEdit")
        config.userContentController.addUserScript(Self.editableScript)

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        #if os(macOS)
        webView.setValue(false, forKey: "drawsBackground")
        #else
        webView.isOpaque = false
        webView.backgroundColor = .black
        webView.scrollView.backgroundColor = .black
        #endif
        return webView
    }

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
        // Only reload if the target URL differs from what's currently loaded.
        if webView.url?.standardizedFileURL == url.standardizedFileURL { return }
        webView.loadFileURL(url, allowingReadAccessTo: root)
    }

    // MARK: - Coordinator — intercepts navigations

    final class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
        let parent: VaultWebView
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

            if url.isFileURL, let root = parent.vaultRoot {
                // Internal vault link — bubble up so VaultModel can update history and sidebar.
                if url.path.hasPrefix(root.path) {
                    decisionHandler(.cancel)
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
