//
//  AppendixE_CryoTunesPlayer.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixE_CryoTunesPlayer: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix E: CryoTunes Player",
            vaultRelativePath: "Appendices/Appendix-E-CryoTunes-Player/Appendix-E-CryoTunes-Player.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixE_CryoTunesPlayer()
        .environmentObject(VaultModel())
}
