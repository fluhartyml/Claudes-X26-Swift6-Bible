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
    /// SwiftUI toolbar can trigger actions (Highlight, Edit toggle) on it.
    final class Bridge: ObservableObject {
        weak var webView: WKWebView?
        /// Edit mode is OFF by default — readers tap links cleanly, no
        /// keyboard pop. Flip ON to scribble notes / edit content.
        @Published var isEditing: Bool = false {
            didSet { applyEditMode() }
        }
        func applyEditMode() {
            let js = "window.setEditMode && window.setEditMode(\(isEditing));"
            webView?.evaluateJavaScript(js)
        }
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

    /// Inject styling for highlights + suppress iOS's native long-press
    /// callout menu when in read mode (we want our own long-press
    /// gesture in editableScript to handle highlighting instead).
    private static let highlightStyleScript: WKUserScript = {
        let source = """
        (function(){
          var s = document.createElement('style');
          s.textContent =
            'mark.user-hl{background:#FFFF00;color:#000;padding:0 0.1em;border-radius:2px;}' +
            'body:not([contenteditable=\"true\"]){-webkit-touch-callout:none;}';
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

          // Edit mode starts OFF — readers tap links cleanly with no
          // keyboard pop. Swift toggles it ON via window.setEditMode(true)
          // when the toolbar pencil is engaged.
          body.contentEditable = 'false';
          body.spellcheck = true;

          window.setEditMode = function(enabled){
            document.body.contentEditable = enabled ? 'true' : 'false';
          };

          // In contentEditable, tapping a link normally puts the cursor
          // inside instead of navigating. Mark every <a> contentEditable=
          // 'false' so taps behave as ordinary link activations and
          // VaultWebView's WKNavigationDelegate picks them up. Harmless
          // when body itself isn't editable; protective when it is.
          function fixLinks(root){
            var links = (root || document).querySelectorAll('a');
            for (var i = 0; i < links.length; i++) {
              links[i].setAttribute('contenteditable', 'false');
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

          // ============================================================
          // Highlight mode: long-press a word to highlight it, drag to
          // extend forward/backward word by word. Long-press an already-
          // highlighted word to remove the highlight. Active only when
          // edit mode is OFF (otherwise normal text-edit interactions
          // win). On long-press start, native iOS callout is suppressed
          // by the body:not([contenteditable=true]) rule in the
          // highlight style script.
          // ============================================================

          function isEditing(){ return document.body.contentEditable === 'true'; }

          function caretPosFromPoint(x, y){
            // Standard:
            if (document.caretPositionFromPoint) {
              var p = document.caretPositionFromPoint(x, y);
              if (p) return { node: p.offsetNode, offset: p.offset };
            }
            // WebKit fallback:
            if (document.caretRangeFromPoint) {
              var r = document.caretRangeFromPoint(x, y);
              if (r) return { node: r.startContainer, offset: r.startOffset };
            }
            return null;
          }

          // Snap a (textNode, offset) pair outward to the nearest word
          // boundary on each side, returning a Range covering the word.
          function wordRangeAt(x, y){
            var p = caretPosFromPoint(x, y);
            if (!p || p.node.nodeType !== 3) return null;
            var text = p.node.nodeValue || '';
            if (!text) return null;
            // Walk left for word start.
            var i = Math.min(p.offset, text.length);
            while (i > 0 && /\\S/.test(text.charAt(i - 1))) i--;
            // Walk right for word end.
            var j = Math.min(p.offset, text.length);
            while (j < text.length && /\\S/.test(text.charAt(j))) j++;
            if (i === j) return null;
            var range = document.createRange();
            range.setStart(p.node, i);
            range.setEnd(p.node, j);
            return range;
          }

          // Combine two word-ranges into a single range spanning the
          // earlier start to the later end. Direction-agnostic so the
          // user can drag forward or backward from the anchor.
          function unionRange(a, b){
            var r = document.createRange();
            var aFirst = a.compareBoundaryPoints(Range.START_TO_START, b) <= 0;
            r.setStart(aFirst ? a.startContainer : b.startContainer, aFirst ? a.startOffset : b.startOffset);
            r.setEnd(aFirst ? b.endContainer : a.endContainer, aFirst ? b.endOffset : a.endOffset);
            return r;
          }

          function isInsideHighlight(node){
            while (node && node !== document.body) {
              if (node.nodeType === 1 && node.tagName === 'MARK' && node.classList && node.classList.contains('user-hl')) {
                return node;
              }
              node = node.parentNode;
            }
            return null;
          }

          function unhighlight(mark){
            var parent = mark.parentNode;
            while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
            parent.removeChild(mark);
            // Re-merge adjacent text nodes for a cleaner DOM.
            parent.normalize && parent.normalize();
            document.body.dispatchEvent(new Event('input', { bubbles: true }));
          }

          // Wrap a Range in a fresh <mark.user-hl>. If the range overlaps
          // existing highlights we'd need merge logic; v1 keeps it simple
          // and trusts the user not to overlap (existing highlights aren't
          // re-highlighted on re-tap because anchor detection finds them
          // first and runs the unhighlight branch).
          function applyHighlightRange(range){
            try {
              var mark = document.createElement('mark');
              mark.className = 'user-hl';
              range.surroundContents(mark);
            } catch(e) {
              // Range crosses element boundaries — fall back to extract.
              var frag = range.extractContents();
              var mark2 = document.createElement('mark');
              mark2.className = 'user-hl';
              mark2.appendChild(frag);
              range.insertNode(mark2);
            }
            document.body.dispatchEvent(new Event('input', { bubbles: true }));
          }

          // Long-press tracking state.
          var pressTimer = null;
          var pressStartX = 0, pressStartY = 0;
          var anchorWordRange = null;     // first highlighted word
          var lastHighlightMark = null;   // mark currently being grown
          var pressedHighlight = null;    // existing mark we long-pressed
          var movedTooEarly = false;

          var LONG_PRESS_MS = 450;
          var MOVE_TOLERANCE_BEFORE = 8;   // px — finger jitter before long-press fires

          function clearPress(){
            if (pressTimer) { clearTimeout(pressTimer); pressTimer = null; }
            anchorWordRange = null;
            lastHighlightMark = null;
            pressedHighlight = null;
            movedTooEarly = false;
          }

          document.addEventListener('touchstart', function(e){
            if (isEditing()) return;
            if (e.touches.length !== 1) return;
            var t = e.touches[0];
            pressStartX = t.clientX;
            pressStartY = t.clientY;
            movedTooEarly = false;

            pressTimer = setTimeout(function(){
              pressTimer = null;
              if (movedTooEarly) return;

              // What did we long-press on? Existing highlight = unhighlight.
              var topEl = document.elementFromPoint(pressStartX, pressStartY);
              var hl = isInsideHighlight(topEl);
              if (hl) {
                pressedHighlight = hl;
                unhighlight(hl);
                return;
              }

              // Otherwise: highlight the word at the press point and
              // remember it as the anchor for drag-to-extend.
              var wr = wordRangeAt(pressStartX, pressStartY);
              if (!wr) return;
              anchorWordRange = wr.cloneRange();
              applyHighlightRange(wr);
              // The wrap created a fresh <mark>; remember it so we can
              // re-shape on touchmove.
              var sel = document.body.querySelector('mark.user-hl:last-of-type');
              lastHighlightMark = sel;
            }, LONG_PRESS_MS);
          }, { passive: true });

          document.addEventListener('touchmove', function(e){
            if (isEditing()) return;
            if (e.touches.length !== 1) return;
            var t = e.touches[0];

            // If we haven't entered highlight mode yet (timer still
            // pending), small movement is fine; large movement cancels
            // the long-press.
            if (pressTimer) {
              var dx = t.clientX - pressStartX;
              var dy = t.clientY - pressStartY;
              if (dx*dx + dy*dy > MOVE_TOLERANCE_BEFORE * MOVE_TOLERANCE_BEFORE) {
                movedTooEarly = true;
                clearTimeout(pressTimer);
                pressTimer = null;
              }
              return;
            }

            // We're in active highlight-drag. Extend the anchor range to
            // include the word currently under the finger.
            if (!anchorWordRange) return;
            var wr = wordRangeAt(t.clientX, t.clientY);
            if (!wr) return;
            // Combine anchor word with current word.
            var combined = unionRange(anchorWordRange, wr);

            // Replace the current highlight with the combined range:
            // unhighlight the old mark, then re-apply on the union.
            if (lastHighlightMark && lastHighlightMark.parentNode) {
              // Walk children out of the old mark.
              var p = lastHighlightMark.parentNode;
              while (lastHighlightMark.firstChild) p.insertBefore(lastHighlightMark.firstChild, lastHighlightMark);
              p.removeChild(lastHighlightMark);
              p.normalize && p.normalize();
              lastHighlightMark = null;
              // Anchor's text node may have been split/merged; re-resolve
              // the anchor word range from the original press point.
              anchorWordRange = wordRangeAt(pressStartX, pressStartY);
              if (!anchorWordRange) return;
              combined = unionRange(anchorWordRange, wr);
            }
            try {
              applyHighlightRange(combined);
              lastHighlightMark = document.body.querySelector('mark.user-hl:last-of-type');
            } catch(e) {
              // Range got too messy (crossed too many element boundaries);
              // bail out gracefully.
            }
          }, { passive: true });

          document.addEventListener('touchend', function(){
            // Finalize: nothing more to do; the highlight mark is in the
            // DOM and the input event already fired so the page will
            // save itself within 1.2s.
            clearPress();
          }, { passive: true });

          document.addEventListener('touchcancel', clearPress, { passive: true });
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
