//
//  AppendixM_CryoKit.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixM_CryoKit: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix M: CryoKit (Shared Package Source Tour)",
            vaultRelativePath: "Appendices/Appendix-M-CryoKit/Appendix-M-CryoKit.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixM_CryoKit()
        .environmentObject(VaultModel())
}
