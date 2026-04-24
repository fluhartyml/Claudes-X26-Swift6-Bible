//
//  BuildAlong14_TipJar.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong14_TipJar: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 14: TipJar",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-14-TipJar/BuildAlong-14-TipJar.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong14_TipJar()
        .environmentObject(VaultModel())
}
