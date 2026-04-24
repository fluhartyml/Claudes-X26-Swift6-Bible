//
//  AppendixK_NightGardDDNS.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixK_NightGardDDNS: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix K: NightGard DDNS (Self-Publishing Case Study)",
            vaultRelativePath: "Appendices/Appendix-K-NightGard-DDNS/Appendix-K-NightGard-DDNS.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixK_NightGardDDNS()
        .environmentObject(VaultModel())
}
