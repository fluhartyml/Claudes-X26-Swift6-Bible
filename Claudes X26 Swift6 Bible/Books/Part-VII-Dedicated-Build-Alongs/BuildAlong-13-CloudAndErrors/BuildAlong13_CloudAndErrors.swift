//
//  BuildAlong13_CloudAndErrors.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong13_CloudAndErrors: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 13: CloudAndErrors",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-13-CloudAndErrors/BuildAlong-13-CloudAndErrors.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong13_CloudAndErrors()
        .environmentObject(VaultModel())
}
