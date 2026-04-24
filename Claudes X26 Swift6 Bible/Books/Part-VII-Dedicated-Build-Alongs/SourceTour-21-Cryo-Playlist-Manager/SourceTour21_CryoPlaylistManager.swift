//
//  SourceTour21_CryoPlaylistManager.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour21_CryoPlaylistManager: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 21: Cryo Playlist Manager",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-21-Cryo-Playlist-Manager/SourceTour-21-Cryo-Playlist-Manager.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour21_CryoPlaylistManager()
        .environmentObject(VaultModel())
}
