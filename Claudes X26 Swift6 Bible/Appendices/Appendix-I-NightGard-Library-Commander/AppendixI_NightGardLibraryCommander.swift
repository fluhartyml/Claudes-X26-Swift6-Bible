//
//  AppendixI_NightGardLibraryCommander.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixI_NightGardLibraryCommander: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix I: NightGard Library Commander",
            vaultRelativePath: "Appendices/Appendix-I-NightGard-Library-Commander/Appendix-I-NightGard-Library-Commander.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixI_NightGardLibraryCommander()
        .environmentObject(VaultModel())
}
