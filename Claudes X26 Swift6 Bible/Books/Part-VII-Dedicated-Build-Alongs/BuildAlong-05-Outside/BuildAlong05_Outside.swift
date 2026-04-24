//
//  BuildAlong05_Outside.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong05_Outside: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 05: Outside",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-05-Outside/BuildAlong-05-Outside.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong05_Outside()
        .environmentObject(VaultModel())
}
