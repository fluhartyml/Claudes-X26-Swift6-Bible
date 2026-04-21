//
//  Book00_BookParameters.swift
//  Claudes X26 Swift6 Bible
//
//  Part I Introduction, Book 00. The editorial rulebook —
//  Citation Standard, Source Requirements, Writing Style, Font,
//  License, Proofing. First thing a reader encounters.
//

import SwiftUI

struct Book00_BookParameters: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 00: Book Parameters",
            vaultRelativePath: "Part-I-Introduction/Book-00-Book-Parameters/Book-00-Book-Parameters.html",
            status: "Written — the rules the book is written by."
        )
    }
}

#Preview {
    Book00_BookParameters()
        .environmentObject(VaultModel())
}
