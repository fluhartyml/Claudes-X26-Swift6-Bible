//
//  BuildAlong00_ClaudesX26Swift6Bible.swift
//  Claudes X26 Swift6 Bible
//
//  Reader App entry — position 00 in Part VII. The reader app you are
//  currently holding. Listed first so readers orient to the book's
//  delivery vehicle before the primary build-alongs.
//

import SwiftUI

struct BuildAlong00_ClaudesX26Swift6Bible: View {
    var body: some View {
        BookPlaceholderView(
            title: "Reader App: Claude's X26 Swift6 Bible (Inkwell)",
            vaultRelativePath: "Part-VII-Dedicated-Build-Alongs/BuildAlong-00-Claudes-X26-Swift6-Bible-Inkwell/BuildAlong-00-Claudes-X26-Swift6-Bible-Inkwell.html",
            status: "Reader app source tour."
        )
    }
}

#Preview {
    BuildAlong00_ClaudesX26Swift6Bible()
        .environmentObject(VaultModel())
}
