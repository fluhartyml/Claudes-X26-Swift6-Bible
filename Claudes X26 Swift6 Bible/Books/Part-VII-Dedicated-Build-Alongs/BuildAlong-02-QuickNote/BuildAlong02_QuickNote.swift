//
//  BuildAlong02_QuickNote.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong02_QuickNote: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 02: QuickNote",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-02-QuickNote/BuildAlong-02-QuickNote.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong02_QuickNote()
        .environmentObject(VaultModel())
}
