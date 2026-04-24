//
//  SourceTour20_SnapAndScanKeeper.swift
//  Claudes X26 Swift6 Bible
//
//  Part VII app entry. Production-app source tour — readers install
//  and browse, they do not build this one from scratch. Thin view
//  pointing at the HTML content in BibleContent.bundle.
//

import SwiftUI

struct SourceTour20_SnapAndScanKeeper: View {
    var body: some View {
        BookPlaceholderView(
            title: "Source Tour 20: Snap & ScanKeeper",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/SourceTour-20-Snap-ScanKeeper/SourceTour-20-Snap-ScanKeeper.html",
            status: "Production-app source tour (install + browse, not build-along)."
        )
    }
}

#Preview {
    SourceTour20_SnapAndScanKeeper()
        .environmentObject(VaultModel())
}
