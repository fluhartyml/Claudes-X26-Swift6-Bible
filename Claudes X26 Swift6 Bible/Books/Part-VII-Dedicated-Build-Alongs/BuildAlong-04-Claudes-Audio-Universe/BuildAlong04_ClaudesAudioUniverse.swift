//
//  BuildAlong04_ClaudesAudioUniverse.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong04_ClaudesAudioUniverse: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 04: Claude's Audio Universe",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-04-Claudes-Audio-Universe/BuildAlong-04-Claudes-Audio-Universe.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong04_ClaudesAudioUniverse()
        .environmentObject(VaultModel())
}
