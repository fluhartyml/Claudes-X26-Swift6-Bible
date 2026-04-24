//
//  SourceTour24_NightGardDDNS.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour24_NightGardDDNS: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 24: NightGard DDNS (Self-Publishing Case Study)",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-24-NightGard-DDNS/SourceTour-24-NightGard-DDNS.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour24_NightGardDDNS()
        .environmentObject(VaultModel())
}
