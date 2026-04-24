//
//  BuildAlong16_ChatWithClaude.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong16_ChatWithClaude: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 16: ChatWithClaude",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-16-ChatWithClaude/BuildAlong-16-ChatWithClaude.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong16_ChatWithClaude()
        .environmentObject(VaultModel())
}
