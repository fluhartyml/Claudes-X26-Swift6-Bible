//
//  BuildAlong08_IntelligenceDemo.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong08_IntelligenceDemo: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 08: IntelligenceDemo",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-08-IntelligenceDemo/BuildAlong-08-IntelligenceDemo.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong08_IntelligenceDemo()
        .environmentObject(VaultModel())
}
