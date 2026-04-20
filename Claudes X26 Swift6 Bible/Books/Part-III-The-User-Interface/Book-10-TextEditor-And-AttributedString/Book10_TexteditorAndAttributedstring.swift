//
//  Book10_TexteditorAndAttributedstring.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book10_TexteditorAndAttributedstring: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 10: TextEditor & AttributedString",
            vaultRelativePath: "Part-III-The-User-Interface/Book-10-TextEditor-And-AttributedString/Book-10-TextEditor-And-AttributedString.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book10_TexteditorAndAttributedstring()
        .environmentObject(VaultModel())
}
