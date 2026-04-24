//
//  BuildAlong17_TvOSAmbientDisplay.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong17_TvOSAmbientDisplay: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 17: tvOS Ambient Display",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-17-tvOS-Ambient-Display/BuildAlong-17-tvOS-Ambient-Display.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong17_TvOSAmbientDisplay()
        .environmentObject(VaultModel())
}
