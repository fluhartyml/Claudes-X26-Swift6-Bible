//
//  Book21_GitAndGithub.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book21_GitAndGithub: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 21: Git & GitHub",
            vaultRelativePath: "Part-VI-The-Modern-Toolchain/Book-21-Git-And-GitHub/Book-21-Git-And-GitHub.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book21_GitAndGithub()
        .environmentObject(VaultModel())
}
