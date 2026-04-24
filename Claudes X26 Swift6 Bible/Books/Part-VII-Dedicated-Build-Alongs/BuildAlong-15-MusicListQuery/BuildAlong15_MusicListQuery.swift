//
//  BuildAlong15_MusicListQuery.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong15_MusicListQuery: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 15: MusicListQuery (Mac)",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-15-MusicListQuery/BuildAlong-15-MusicListQuery.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong15_MusicListQuery()
        .environmentObject(VaultModel())
}
