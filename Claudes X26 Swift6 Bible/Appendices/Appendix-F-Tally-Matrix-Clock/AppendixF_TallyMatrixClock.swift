//
//  AppendixF_TallyMatrixClock.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixF_TallyMatrixClock: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix F: Tally Matrix Clock",
            vaultRelativePath: "Appendices/Appendix-F-Tally-Matrix-Clock/Appendix-F-Tally-Matrix-Clock.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixF_TallyMatrixClock()
        .environmentObject(VaultModel())
}
