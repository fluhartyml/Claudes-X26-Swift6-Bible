//
//  SourceTour22_NightGardLibraryCommander.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour22_NightGardLibraryCommander: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 22: NightGard Library Commander",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-22-NightGard-Library-Commander/SourceTour-22-NightGard-Library-Commander.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour22_NightGardLibraryCommander()
        .environmentObject(VaultModel())
}
