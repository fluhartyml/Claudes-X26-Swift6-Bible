//
//  AppendixB_WebWrapper.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct AppendixB_WebWrapper: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix B: Claude's Web Wrapper",
            vaultRelativePath: "Appendices/Appendix-B-Claudes-Web-Wrapper/Appendix-B-Claudes-Web-Wrapper.html",
            status: "Placeholder — existing file at vault root: appendix-claudes-web-wrapper-v2.html"
        )
    }
}

#Preview {
    AppendixB_WebWrapper()
        .environmentObject(VaultModel())
}
