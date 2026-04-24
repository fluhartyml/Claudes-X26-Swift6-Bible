//
//  BuildAlong03_ClaudesLockBox.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong03_ClaudesLockBox: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 03: Claude's LockBox",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-03-Claudes-LockBox/BuildAlong-03-Claudes-LockBox.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong03_ClaudesLockBox()
        .environmentObject(VaultModel())
}
