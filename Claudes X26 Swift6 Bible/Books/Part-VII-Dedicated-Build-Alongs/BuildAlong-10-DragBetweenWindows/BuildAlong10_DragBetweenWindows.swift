//
//  BuildAlong10_DragBetweenWindows.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong10_DragBetweenWindows: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 10: DragBetweenWindows",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-10-DragBetweenWindows/BuildAlong-10-DragBetweenWindows.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong10_DragBetweenWindows()
        .environmentObject(VaultModel())
}
