//
//  VaultModel.swift
//  Claudes X26 Swift6 Bible
//
//  State model for the Bible vault — holds the vault root URL,
//  the file tree, the currently-open document, and navigation history.
//

import Foundation
import SwiftUI
import Combine
#if os(macOS)
import AppKit
#else
import UIKit
#endif

@MainActor
final class VaultModel: ObservableObject {

    // MARK: - Published state

    @Published var vaultRoot: URL?
    @Published var rootNode: VaultNode?
    @Published var currentDocument: URL?
    @Published var selectedNodeID: VaultNode.ID?
    @Published var expandedNodeIDs: Set<VaultNode.ID> = []

    func toggleExpanded(_ id: VaultNode.ID) {
        if expandedNodeIDs.contains(id) {
            expandedNodeIDs.remove(id)
        } else {
            expandedNodeIDs.insert(id)
        }
    }

    /// Print a tap/navigation event to the Xcode console so Michael can
    /// trace which buttons/links routed through the app. Prefix tells
    /// the source layer (Folder / File / Link / Open).
    func logTap(_ message: String) {
        print("[tap] \(message)")
    }

    private var history: [URL] = []
    private var forwardHistory: [URL] = []

    // MARK: - Defaults keys

    private let bookmarkKey = "vaultRootBookmark"
    private let lastPathKey = "lastDocumentPath"

    // MARK: - Init

    init() {
        resolveVaultRoot()
    }

    // MARK: - Vault-root resolution

    /// Try to locate a vault root on launch. Priority:
    ///  1. Security-scoped bookmark (user-picked vault).
    ///  2. Extracted vault in Application Support (works on both iOS + macOS).
    ///  3. Bundled BibleContent.bundle (macOS filesystem-sync preserves it).
    ///  4. nil — user must pick.
    private func resolveVaultRoot() {
        if let url = restoreBookmarkedRoot() {
            setVaultRoot(url)
            return
        }
        if let extracted = VaultBundleExtractor.ensureExtracted(),
           FileManager.default.fileExists(atPath: extracted.appending(path: "table-of-contents.html").path) {
            setVaultRoot(extracted)
            return
        }
        if let bundled = Bundle.main.url(forResource: "BibleContent", withExtension: "bundle") {
            setVaultRoot(bundled)
            return
        }
    }

    private func restoreBookmarkedRoot() -> URL? {
        guard let data = UserDefaults.standard.data(forKey: bookmarkKey) else { return nil }
        var stale = false
        #if os(macOS)
        let options: URL.BookmarkResolutionOptions = [.withSecurityScope]
        #else
        let options: URL.BookmarkResolutionOptions = []
        #endif
        guard let url = try? URL(
            resolvingBookmarkData: data,
            options: options,
            relativeTo: nil,
            bookmarkDataIsStale: &stale
        ) else { return nil }
        _ = url.startAccessingSecurityScopedResource()
        return url
    }

    func setVaultRoot(_ url: URL) {
        vaultRoot = url
        rootNode = VaultNode.buildTree(at: url)
        // Priority: last document the reader viewed > table of contents > atlas.
        if let lastRel = UserDefaults.standard.string(forKey: lastPathKey) {
            let lastURL = url.appending(path: lastRel)
            if FileManager.default.fileExists(atPath: lastURL.path) {
                currentDocument = lastURL
                return
            }
        }
        let tocURL = url.appending(path: "table-of-contents.html")
        if FileManager.default.fileExists(atPath: tocURL.path) {
            currentDocument = tocURL
        } else {
            let indexURL = url.appending(path: "claudex26-index.html")
            if FileManager.default.fileExists(atPath: indexURL.path) {
                currentDocument = indexURL
            }
        }
    }

    private func saveLastDocument(_ url: URL) {
        guard let root = vaultRoot else { return }
        let rootPath = root.path
        let docPath = url.path
        guard docPath.hasPrefix(rootPath) else { return }
        var rel = String(docPath.dropFirst(rootPath.count))
        if rel.hasPrefix("/") { rel = String(rel.dropFirst()) }
        UserDefaults.standard.set(rel, forKey: lastPathKey)
    }

    /// Save a security-scoped bookmark to the chosen URL so next launch restores it.
    private func saveBookmark(for url: URL) {
        #if os(macOS)
        let options: URL.BookmarkCreationOptions = [.withSecurityScope]
        #else
        let options: URL.BookmarkCreationOptions = []
        #endif
        if let data = try? url.bookmarkData(
            options: options,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        ) {
            UserDefaults.standard.set(data, forKey: bookmarkKey)
        }
    }

    // MARK: - Picker

    func chooseVaultRoot() {
        #if os(macOS)
        let panel = NSOpenPanel()
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = false
        panel.message = "Choose the Bible vault folder."
        panel.prompt = "Open"
        if panel.runModal() == .OK, let url = panel.url {
            _ = url.startAccessingSecurityScopedResource()
            saveBookmark(for: url)
            setVaultRoot(url)
        }
        #endif
        // iOS/iPadOS picker is surfaced from ContentView via .fileImporter modifier.
    }

    func handlePickedFolder(_ url: URL) {
        _ = url.startAccessingSecurityScopedResource()
        saveBookmark(for: url)
        setVaultRoot(url)
    }

    // MARK: - Navigation

    func open(_ relativePath: String) {
        guard let root = vaultRoot else { return }
        let url = root.appending(path: relativePath)
        open(url)
    }

    func open(_ url: URL) {
        logTap("Open: \(url.lastPathComponent)")
        if let cur = currentDocument {
            history.append(cur)
        }
        forwardHistory.removeAll()
        currentDocument = url
        saveLastDocument(url)
    }

    func goBack() {
        guard let prev = history.popLast() else { return }
        if let cur = currentDocument {
            forwardHistory.append(cur)
        }
        currentDocument = prev
    }

    func goForward() {
        guard let next = forwardHistory.popLast() else { return }
        if let cur = currentDocument {
            history.append(cur)
        }
        currentDocument = next
    }

    var canGoBack: Bool { !history.isEmpty }
    var canGoForward: Bool { !forwardHistory.isEmpty }

    func goHome() {
        open("table-of-contents.html")
    }

    // MARK: - Display

    func displayPath(for url: URL) -> String {
        let stripped = (url.lastPathComponent as NSString).deletingPathExtension
        let ext = url.pathExtension
        guard let root = vaultRoot else { return stripped }
        let rootPath = root.path
        let fullPath = url.path
        if fullPath.hasPrefix(rootPath) {
            var rel = String(fullPath.dropFirst(rootPath.count))
            if rel.hasPrefix("/") { rel.removeFirst() }
            // Strip the extension from the last component only — paths
            // display without ".html" per the universal page template rule.
            if !ext.isEmpty, rel.hasSuffix("." + ext) {
                rel.removeLast(ext.count + 1)
            }
            return rel
        }
        return stripped
    }
}

// MARK: - Vault file tree

struct VaultNode: Identifiable, Hashable {
    let id: URL
    let url: URL
    let name: String
    let isDirectory: Bool
    var children: [VaultNode]

    /// Extension icon suggestion (SF Symbol name).
    var symbolName: String {
        if isDirectory { return "folder" }
        switch url.pathExtension.lowercased() {
        case "html", "htm": return "doc.richtext"
        case "md":          return "doc.text"
        case "png", "jpg", "jpeg", "gif", "svg": return "photo"
        case "epub":        return "book.closed"
        case "swift":       return "swift"
        case "pdf":         return "doc"
        default:            return "doc"
        }
    }

    static func buildTree(at url: URL) -> VaultNode? {
        let fm = FileManager.default
        var isDir: ObjCBool = false
        guard fm.fileExists(atPath: url.path, isDirectory: &isDir) else { return nil }

        if !isDir.boolValue {
            return VaultNode(id: url, url: url, name: url.lastPathComponent, isDirectory: false, children: [])
        }

        let children: [VaultNode]
        do {
            let entries = try fm.contentsOfDirectory(
                at: url,
                includingPropertiesForKeys: [.isDirectoryKey],
                options: [.skipsHiddenFiles]
            )
            .filter { shouldShowInSidebar($0) }
            .sorted { lhs, rhs in
                // Known items (TOC, Parts, Appendices, figures) take their
                // logical sort key; other files/folders go to the end
                // alphabetically. A known file can outrank a directory,
                // so we compare the sortKey first before falling back to
                // directories-first.
                let lKey = sortKey(lhs.lastPathComponent)
                let rKey = sortKey(rhs.lastPathComponent)
                if lKey != rKey { return lKey < rKey }
                let lIsDir = (try? lhs.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) ?? false
                let rIsDir = (try? rhs.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) ?? false
                if lIsDir != rIsDir { return lIsDir }
                return lhs.lastPathComponent.localizedStandardCompare(rhs.lastPathComponent) == .orderedAscending
            }
            children = entries.compactMap { buildTree(at: $0) }
        } catch {
            children = []
        }
        return VaultNode(id: url, url: url, name: url.lastPathComponent, isDirectory: true, children: children)
    }

    /// Logical-reading-order sort key for top-level vault items.
    /// Lower number sorts earlier. Unknowns fall through to alphabetical.
    private static func sortKey(_ name: String) -> Int {
        if name == "table-of-contents.html" { return 1 }  // #1 in the sidebar
        if name == "Front-Matter"      { return 5 }   // before Part I
        if name.hasPrefix("Part-I-")   { return 10 }
        if name.hasPrefix("Part-II-")  { return 20 }
        if name.hasPrefix("Part-III-") { return 30 }
        if name.hasPrefix("Part-IV-")  { return 40 }
        if name.hasPrefix("Part-V-")   { return 50 }
        if name.hasPrefix("Part-VI-")  { return 60 }
        if name == "Appendices"        { return 90 }
        if name == "figures"           { return 95 }   // appendix-style image gallery
        return 100
    }

    /// Whether a URL should appear in the sidebar file tree.
    /// Hides raw Markdown sources, asset folders, build scripts, and
    /// legacy root-level duplicates.
    private static func shouldShowInSidebar(_ url: URL) -> Bool {
        let name = url.lastPathComponent
        if name.hasPrefix(".") { return false }
        if name.hasPrefix("_build-") { return false }
        if name.hasSuffix(".md") { return false }                 // raw Markdown sources
        if name == "cover.jpg" { return false }
        if name == "Screenshots" { return false }                 // asset folder
        if name == "_shared" { return false }                     // shared assets
        // Legacy root-level HTML duplicates of the Appendix content.
        if name.hasPrefix("appendix-") && name.hasSuffix(".html") { return false }
        return true
    }
}
