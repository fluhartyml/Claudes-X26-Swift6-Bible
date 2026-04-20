//
//  Book17_SwiftChartsAndPdfkit.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct Book17_SwiftChartsAndPdfkit: View {
    var body: some View {
        BookPlaceholderView(
            title: "Book 17: Swift Charts & PDFKit",
            vaultRelativePath: "Part-IV-The-Application/Book-17-Swift-Charts-And-PDFKit/Book-17-Swift-Charts-And-PDFKit.html",
            status: "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
        )
    }
}

#Preview {
    Book17_SwiftChartsAndPdfkit()
        .environmentObject(VaultModel())
}
