//
//  PageSendable.swift
//  Claudes X26 Swift6 Bible
//
//  Page: @Sendable  (Chapter S, kind: attribute)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageSendable: View {
    var body: some View {
        PagePlaceholderView(
            headword: "@Sendable",
            chapter: "S",
            kind: "attribute"
        )
    }
}

#Preview {
    PageSendable()
}
