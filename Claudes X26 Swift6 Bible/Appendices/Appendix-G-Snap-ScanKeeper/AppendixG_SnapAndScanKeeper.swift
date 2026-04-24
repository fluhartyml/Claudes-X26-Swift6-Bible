//
//  AppendixG_SnapAndScanKeeper.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixG_SnapAndScanKeeper: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix G: Snap & ScanKeeper",
            vaultRelativePath: "Appendices/Appendix-G-Snap-ScanKeeper/Appendix-G-Snap-ScanKeeper.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixG_SnapAndScanKeeper()
        .environmentObject(VaultModel())
}
