//
//  BuildAlong12_SwiftUICraft.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong12_SwiftUICraft: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 12: SwiftUICraft",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-12-SwiftUICraft/BuildAlong-12-SwiftUICraft.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong12_SwiftUICraft()
        .environmentObject(VaultModel())
}
