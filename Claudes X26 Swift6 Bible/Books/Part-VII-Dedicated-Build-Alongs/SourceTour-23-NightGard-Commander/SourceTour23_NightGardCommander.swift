//
//  SourceTour23_NightGardCommander.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour23_NightGardCommander: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 23: NightGard Commander (Self-Publishing Case Study)",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-23-NightGard-Commander/SourceTour-23-NightGard-Commander.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour23_NightGardCommander()
        .environmentObject(VaultModel())
}
