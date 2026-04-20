//
//  AppendixD_LockBox.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct AppendixD_LockBox: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix D: Claude's LockBox",
            vaultRelativePath: "Appendices/Appendix-D-LockBox/Appendix-D-LockBox.html",
            status: "Placeholder — not yet written."
        )
    }
}

#Preview {
    AppendixD_LockBox()
        .environmentObject(VaultModel())
}
