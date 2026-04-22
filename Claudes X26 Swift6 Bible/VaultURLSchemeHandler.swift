//
//  VaultURLSchemeHandler.swift
//  Claudes X26 Swift6 Bible
//
//  Serves vault content to WKWebView via a custom "bible://" URL scheme
//  so we bypass iOS's file:// sandbox-extension quirks. Every request
//  resolves against the live vaultRoot; subsequent loads in subdirectories
//  succeed without needing to re-widen allowingReadAccessTo.
//

import Foundation
import WebKit
import UniformTypeIdentifiers

final class VaultURLSchemeHandler: NSObject, WKURLSchemeHandler {
    static let scheme = "bible"

    private let rootProvider: () -> URL?

    init(rootProvider: @escaping () -> URL?) {
        self.rootProvider = rootProvider
    }

    /// Convert a vault-local file URL to its bible:// equivalent.
    static func url(for file: URL, root: URL) -> URL? {
        let rootPath = root.resolvingSymlinksInPath().path
        let filePath = file.resolvingSymlinksInPath().path
        guard filePath.hasPrefix(rootPath) else { return nil }
        var rel = String(filePath.dropFirst(rootPath.count))
        if rel.hasPrefix("/") { rel.removeFirst() }
        // Percent-encode each path component individually.
        let encoded = rel.split(separator: "/").map { seg -> String in
            String(seg).addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? String(seg)
        }.joined(separator: "/")
        return URL(string: "\(scheme)://vault/\(encoded)")
    }

    /// Reverse: take a bible:// URL and return the on-disk file URL.
    static func fileURL(for schemeURL: URL, root: URL) -> URL? {
        guard schemeURL.scheme == scheme else { return nil }
        var rel = schemeURL.path
        if rel.hasPrefix("/") { rel.removeFirst() }
        guard let decoded = rel.removingPercentEncoding else { return nil }
        return root.appending(path: decoded)
    }

    // MARK: - WKURLSchemeHandler

    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let requestURL = urlSchemeTask.request.url,
              let root = rootProvider(),
              let fileURL = Self.fileURL(for: requestURL, root: root) else {
            urlSchemeTask.didFailWithError(NSError(
                domain: "VaultURLSchemeHandler", code: 404,
                userInfo: [NSLocalizedDescriptionKey: "Vault file not found"]
            ))
            return
        }

        do {
            let data = try Data(contentsOf: fileURL)
            let mime = mimeType(for: fileURL)
            let response = HTTPURLResponse(
                url: requestURL,
                statusCode: 200,
                httpVersion: "HTTP/1.1",
                headerFields: [
                    "Content-Type": mime,
                    "Content-Length": "\(data.count)",
                    "Cache-Control": "no-cache"
                ]
            ) ?? URLResponse(url: requestURL, mimeType: mime, expectedContentLength: data.count, textEncodingName: "utf-8")
            urlSchemeTask.didReceive(response)
            urlSchemeTask.didReceive(data)
            urlSchemeTask.didFinish()
        } catch {
            urlSchemeTask.didFailWithError(error)
        }
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {
        // No-op: we serve synchronously above.
    }

    // MARK: - MIME type guessing

    private func mimeType(for url: URL) -> String {
        let ext = url.pathExtension.lowercased()
        switch ext {
        case "html", "htm": return "text/html; charset=utf-8"
        case "css":         return "text/css; charset=utf-8"
        case "js":          return "application/javascript; charset=utf-8"
        case "json":        return "application/json; charset=utf-8"
        case "svg":         return "image/svg+xml"
        case "png":         return "image/png"
        case "jpg", "jpeg": return "image/jpeg"
        case "gif":         return "image/gif"
        case "webp":        return "image/webp"
        case "pdf":         return "application/pdf"
        case "woff":        return "font/woff"
        case "woff2":       return "font/woff2"
        case "ttf":         return "font/ttf"
        case "otf":         return "font/otf"
        case "md":          return "text/markdown; charset=utf-8"
        default:
            if let type = UTType(filenameExtension: ext),
               let mime = type.preferredMIMEType {
                return mime
            }
            return "application/octet-stream"
        }
    }
}
