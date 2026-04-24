//
//  BuildAlong06_BodyReadings.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong06_BodyReadings: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 06: BodyReadings",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-06-BodyReadings/BuildAlong-06-BodyReadings.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong06_BodyReadings()
        .environmentObject(VaultModel())
}
