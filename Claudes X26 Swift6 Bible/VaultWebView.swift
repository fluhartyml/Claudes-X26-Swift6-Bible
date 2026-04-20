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
    let onInternalNavigate: (URL) -> Void

    // MARK: - Platform bridges

    #if os(macOS)
    func makeNSView(context: Context) -> WKWebView { makeWebView(context: context) }
    func updateNSView(_ webView: WKWebView, context: Context) { loadIfNeeded(webView) }
    #else
    func makeUIView(context: Context) -> WKWebView { makeWebView(context: context) }
    func updateUIView(_ webView: WKWebView, context: Context) { loadIfNeeded(webView) }
    #endif

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    // MARK: - Shared

    private func makeWebView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences.allowsContentJavaScript = true
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

    private func loadIfNeeded(_ webView: WKWebView) {
        guard let url = documentURL, let root = vaultRoot else { return }
        // Only reload if the target URL differs from what's currently loaded.
        if webView.url?.standardizedFileURL == url.standardizedFileURL { return }
        webView.loadFileURL(url, allowingReadAccessTo: root)
    }

    // MARK: - Coordinator — intercepts navigations

    final class Coordinator: NSObject, WKNavigationDelegate {
        let parent: VaultWebView
        init(_ parent: VaultWebView) { self.parent = parent }

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
