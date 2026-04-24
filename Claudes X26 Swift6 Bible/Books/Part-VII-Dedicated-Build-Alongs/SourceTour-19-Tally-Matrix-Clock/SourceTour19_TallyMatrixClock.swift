//
//  SourceTour19_TallyMatrixClock.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour19_TallyMatrixClock: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 19: Tally Matrix Clock",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-19-Tally-Matrix-Clock/SourceTour-19-Tally-Matrix-Clock.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour19_TallyMatrixClock()
        .environmentObject(VaultModel())
}
