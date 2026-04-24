//
//  AppendixB_CryoKit.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixB_CryoKit: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix B: CryoKit (Shared Package Source Tour)",
            vaultRelativePath: "Appendices/Appendix-B-CryoKit/Appendix-B-CryoKit.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixB_CryoKit()
        .environmentObject(VaultModel())
}
