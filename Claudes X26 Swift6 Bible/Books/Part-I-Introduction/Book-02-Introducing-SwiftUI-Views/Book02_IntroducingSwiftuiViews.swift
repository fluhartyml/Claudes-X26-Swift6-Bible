//
//  Book02_IntroducingSwiftuiViews.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book02_IntroducingSwiftuiViews: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 02: SwiftUI Views",
            vaultRelativePath: "Part-I-Introduction/Book-02-Introducing-SwiftUI-Views/Book-02-Introducing-SwiftUI-Views.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book02_IntroducingSwiftuiViews()
        .environmentObject(VaultModel())
}
