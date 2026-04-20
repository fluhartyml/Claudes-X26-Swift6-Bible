//
//  BookPlaceholderView.swift
//  Claudes X26 Swift6 Bible
//
//  Shared view used by every Book's Swift file. Each Book is its own
//  Swift file (see feedback_each_book_own_swift_file.md memory for the
//  organizing principle). The Book's file is a thin View that tells
//  this placeholder what title / vault path / status to show.
//
//  When a Book's content migrates from HTML-in-the-vault to native
//  SwiftUI, the Book's Swift file stops using this placeholder and
//  instead renders the content directly — but the folder/file name
//  stays the same.
//

import SwiftUI

struct BookPlaceholderView: View {
    @EnvironmentObject var vault: VaultModel

    let title: String
    /// Path to the Book's HTML file relative to the vault root.
    let vaultRelativePath: String
    let status: String

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(title)
                .font(.largeTitle.weight(.semibold))
            Text(status)
                .font(.callout)
                .foregroundStyle(.secondary)

            Divider()

            Text("Content lives in the vault at:")
                .font(.headline)
            Text(vaultRelativePath)
                .font(.body.monospaced())
                .padding(8)
                .background(Color.black.opacity(0.3))
                .cornerRadius(6)

            if vault.vaultRoot != nil {
                Button {
                    vault.open(vaultRelativePath)
                } label: {
                    Label("Open in Reader", systemImage: "arrow.up.right.square")
                }
                .buttonStyle(.borderedProminent)
            } else {
                Text("Open the vault from the sidebar to read this Book.")
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }

            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}
