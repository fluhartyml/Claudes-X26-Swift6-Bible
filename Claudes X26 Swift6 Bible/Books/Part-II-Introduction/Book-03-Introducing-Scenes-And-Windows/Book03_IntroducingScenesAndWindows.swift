//
//  Book03_IntroducingScenesAndWindows.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book03_IntroducingScenesAndWindows: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 03: Introducing Scenes & Windows",
            vaultRelativePath: "Part-II-Introduction/Book-03-Introducing-Scenes-And-Windows/Book-03-Introducing-Scenes-And-Windows.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book03_IntroducingScenesAndWindows()
        .environmentObject(VaultModel())
}
