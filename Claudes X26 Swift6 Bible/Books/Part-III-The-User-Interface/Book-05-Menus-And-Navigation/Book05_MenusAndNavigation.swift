//
//  Book05_MenusAndNavigation.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book05_MenusAndNavigation: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 05: Menus & Navigation",
            vaultRelativePath: "Part-III-The-User-Interface/Book-05-Menus-And-Navigation/Book-05-Menus-And-Navigation.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book05_MenusAndNavigation()
        .environmentObject(VaultModel())
}
