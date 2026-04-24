//
//  BuildAlong01_ClaudesWebWrapper.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong01_ClaudesWebWrapper: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 01: Claude's Web Wrapper",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-01-Claudes-Web-Wrapper/BuildAlong-01-Claudes-Web-Wrapper.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong01_ClaudesWebWrapper()
        .environmentObject(VaultModel())
}
