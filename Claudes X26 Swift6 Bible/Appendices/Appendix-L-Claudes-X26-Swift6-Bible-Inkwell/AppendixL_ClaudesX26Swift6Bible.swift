//
//  AppendixL_ClaudesX26Swift6Bible.swift
//  Claudes X26 Swift6 Bible
//
//  Each Appendix is its own Swift file. This file is the organizational
//  home for this Appendix; the actual content lives as HTML at the
//  vault path shown below and is rendered via BookPlaceholderView.
//

import SwiftUI

struct AppendixL_ClaudesX26Swift6Bible: View {
    var body: some View {
        BookPlaceholderView(
            title: "Appendix L: Claude's X26 Swift6 Bible (Inkwell App)",
            vaultRelativePath: "Appendices/Appendix-L-Claudes-X26-Swift6-Bible-Inkwell/Appendix-L-Claudes-X26-Swift6-Bible-Inkwell.html",
            status: "Source tour."
        )
    }
}

#Preview {
    AppendixL_ClaudesX26Swift6Bible()
        .environmentObject(VaultModel())
}
