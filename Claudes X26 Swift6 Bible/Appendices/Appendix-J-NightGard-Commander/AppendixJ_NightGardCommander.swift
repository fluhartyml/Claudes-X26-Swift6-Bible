//
//  AppendixJ_NightGardCommander.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixJ_NightGardCommander: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix J: NightGard Commander (Self-Publishing Case Study)",
            vaultRelativePath: "Appendices/Appendix-J-NightGard-Commander/Appendix-J-NightGard-Commander.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixJ_NightGardCommander()
        .environmentObject(VaultModel())
}
