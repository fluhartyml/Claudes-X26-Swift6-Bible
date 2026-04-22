//
//  VaultBundleExtractor.swift
//  Claudes X26 Swift6 Bible
//
//  Xcode's filesystem-sync flattens non-Swift files into the app bundle
//  root on iOS, so the .bundle-extension trick that preserves folder
//  structure on macOS doesn't carry over. This extractor reconstructs
//  the canonical vault folder tree in Application Support on first
//  launch by classifying each flat-bundled resource by filename and
//  copying it to its expected relative path.
//
//  Idempotent: if the extracted tree already contains the entry-point
//  document (table-of-contents.html), extraction is skipped.
//

import Foundation

enum VaultBundleExtractor {
    static let folderName = "BibleContent"
    /// Bump this when content mapping rules change so the next launch re-extracts.
    static let currentVersion = 24
    private static let versionFileName = ".extraction-version"

    /// Make sure the extracted vault exists at a known location, then return
    /// its URL. Returns nil only if the file system refuses Application Support.
    static func ensureExtracted() -> URL? {
        let fm = FileManager.default
        guard let support = try? fm.url(
            for: .applicationSupportDirectory,
            in: .userDomainMask,
            appropriateFor: nil,
            create: true
        ) else { return nil }

        let root = support.appending(path: folderName)

        if isCurrentVersion(at: root),
           fm.fileExists(atPath: root.appending(path: "table-of-contents.html").path) {
            return root
        }

        try? fm.removeItem(at: root)
        try? fm.createDirectory(at: root, withIntermediateDirectories: true)

        guard let resourcesPath = Bundle.main.resourcePath else { return root }
        let resourcesURL = URL(fileURLWithPath: resourcesPath)

        let enumerator = fm.enumerator(
            at: resourcesURL,
            includingPropertiesForKeys: [.isRegularFileKey],
            options: [.skipsHiddenFiles]
        )

        while let url = enumerator?.nextObject() as? URL {
            let vals = try? url.resourceValues(forKeys: [.isRegularFileKey])
            guard vals?.isRegularFile == true else { continue }
            let name = url.lastPathComponent
            guard let rel = targetPath(forFlat: name) else { continue }
            let dest = root.appending(path: rel)
            try? fm.createDirectory(
                at: dest.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            try? fm.copyItem(at: url, to: dest)
        }

        writeVersion(to: root)
        return root
    }

    // MARK: - Version tracking

    private static func isCurrentVersion(at root: URL) -> Bool {
        let vf = root.appending(path: versionFileName)
        guard let s = try? String(contentsOf: vf, encoding: .utf8),
              let v = Int(s.trimmingCharacters(in: .whitespacesAndNewlines)) else {
            return false
        }
        return v == currentVersion
    }

    private static func writeVersion(to root: URL) {
        let vf = root.appending(path: versionFileName)
        try? "\(currentVersion)".write(to: vf, atomically: true, encoding: .utf8)
    }

    // MARK: - Flat-filename → vault-relative-path mapping

    /// Returns the relative path inside the extracted vault where a
    /// flat-bundled file should live. Returns nil for files we skip
    /// (app binary, Info.plist, asset catalog output, etc.).
    static func targetPath(forFlat filename: String) -> String? {
        // Root-level mapping docs and metadata.
        let rootExact: Set<String> = [
            "claudex26-index.html",
            "claudex26-roadmap.html",
            "swift-section-mapping.html",
            "table-of-contents.html",
            "BOOK-PARAMETERS.md",
            "INDEX.md",
            "cover.jpg",
            "appendix-github-setup.html",
            "appendix-github-setup.md",
            "appendix-claudes-web-wrapper-v2.html",
            "appendix-claudes-web-wrapper.md",
            "appendix-quicknote.md",
        ]
        if rootExact.contains(filename) { return filename }

        // Front of Book — Claude-X26-Parameters.html lives under Front-of-Book/.
        if filename == "Claude-X26-Parameters.html" {
            return "Front-of-Book/\(filename)"
        }

        // Markdown chapter sources "01-*.md" through "22-*.md".
        if filename.hasSuffix(".md"),
           let first = filename.first, first.isNumber,
           let second = filename.dropFirst().first, second.isNumber,
           filename.count > 3, filename[filename.index(filename.startIndex, offsetBy: 2)] == "-" {
            return filename
        }

        // Older chapter drafts (chapter01-04).
        if filename.hasPrefix("chapter0"), filename.hasSuffix(".md") {
            return filename
        }

        // Swift Lexicon Pages — Page-*.html land directly inside
        // Part-II-The-Swift-Language/Chapter-{X}/. The chapter letter is
        // the first alphabetic character of the entry name (after "Page-"),
        // uppercased; e.g. Page-actor.html -> Chapter A, Page-State.html
        // -> Chapter S, Page-Predicate.html -> Chapter P.
        if filename.hasPrefix("Page-"), filename.hasSuffix(".html") {
            let rest = filename.dropFirst("Page-".count)
            if let firstChar = rest.first {
                let letter = String(firstChar).uppercased()
                if letter.count == 1,
                   let scalar = letter.unicodeScalars.first,
                   CharacterSet.uppercaseLetters.contains(scalar) {
                    return "Part-II-The-Swift-Language/Chapter-\(letter)/\(filename)"
                }
            }
        }

        // Numbered Books — Book-NN-*.html. Lands flat under its Part folder
        // (no per-Book sub-folder).
        if filename.hasPrefix("Book-"), filename.hasSuffix(".html") {
            let rest = filename.dropFirst("Book-".count)
            let digits = rest.prefix { $0.isNumber }
            if let num = Int(digits) {
                let partFolder: String
                switch num {
                case 1...3:   partFolder = "Part-I-Introduction"
                case 4...12:  partFolder = "Part-III-The-User-Interface"
                case 13...17: partFolder = "Part-IV-The-Application"
                case 18...20: partFolder = "Part-V-Advanced-Techniques"
                case 21...22: partFolder = "Part-VI-The-Modern-Toolchain"
                default: return nil
                }
                return "\(partFolder)/\(filename)"
            }
        }

        // Appendices — Appendix-X-*.html lands flat under Appendices/.
        if filename.hasPrefix("Appendix-"), filename.hasSuffix(".html") {
            return "Appendices/\(filename)"
        }

        // Figures / screenshots — keep them in a figures subfolder.
        let imageExts: Set<String> = ["png", "jpg", "jpeg", "gif", "svg"]
        if let dot = filename.lastIndex(of: "."),
           imageExts.contains(String(filename[filename.index(after: dot)...]).lowercased()),
           filename != "cover.jpg",
           filename != "AppIcon-iOS.png" {
            return "figures/\(filename)"
        }

        return nil
    }
}
