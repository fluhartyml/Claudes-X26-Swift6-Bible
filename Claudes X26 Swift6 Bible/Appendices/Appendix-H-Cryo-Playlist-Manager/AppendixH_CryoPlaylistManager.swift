//
//  AppendixH_CryoPlaylistManager.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixH_CryoPlaylistManager: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix H: Cryo Playlist Manager",
            vaultRelativePath: "Appendices/Appendix-H-Cryo-Playlist-Manager/Appendix-H-Cryo-Playlist-Manager.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixH_CryoPlaylistManager()
        .environmentObject(VaultModel())
}
