//
//  BuildAlong07_MyPerson.swift
//  Claudes X26 Swift6 Bible
//
//  Each Build-Along is its own Swift file. This file is the
//  organizational home for this build-along; the actual roadmap lives
//  as HTML at the vault path shown below and is rendered via
//  BookPlaceholderView / WKWebView.
//

import SwiftUI

struct BuildAlong07_MyPerson: View {
    var body: some View {
        BookPlaceholderView(
            title: "Build-Along 07: MyPerson",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-07-MyPerson/BuildAlong-07-MyPerson.html",
            status: "Build-along roadmap."
        )
    }
}

#Preview {
    BuildAlong07_MyPerson()
        .environmentObject(VaultModel())
}
