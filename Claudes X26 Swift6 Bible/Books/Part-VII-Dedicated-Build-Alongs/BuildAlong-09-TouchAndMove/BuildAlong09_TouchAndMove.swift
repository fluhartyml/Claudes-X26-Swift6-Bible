//
//  BuildAlong09_TouchAndMove.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong09_TouchAndMove: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 09: TouchAndMove",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-09-TouchAndMove/BuildAlong-09-TouchAndMove.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong09_TouchAndMove()
        .environmentObject(VaultModel())
}
