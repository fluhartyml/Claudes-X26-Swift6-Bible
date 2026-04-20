//
//  AppendixA_GitHubSetup.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct AppendixA_GitHubSetup: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix A: GitHub Setup",
            vaultRelativePath: "Appendices/Appendix-A-GitHub-Setup/Appendix-A-GitHub-Setup.html",
            status: "Placeholder — existing file at vault root: appendix-github-setup.html"
        )
    }
}

#Preview {
    AppendixA_GitHubSetup()
        .environmentObject(VaultModel())
}
