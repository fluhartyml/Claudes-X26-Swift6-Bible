//
//  SourceTour18_CryoTunesPlayer.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour18_CryoTunesPlayer: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 18: CryoTunes Player",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-18-CryoTunes-Player/SourceTour-18-CryoTunes-Player.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour18_CryoTunesPlayer()
        .environmentObject(VaultModel())
}
