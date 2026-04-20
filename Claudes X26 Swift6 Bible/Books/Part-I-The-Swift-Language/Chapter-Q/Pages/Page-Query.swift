//
//  PageQuery.swift
//  Claudes X26 Swift6 Bible
//
//  Page: @Query  (Chapter Q, kind: attribute-swiftdata)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageQuery: View {
    var body: some View {
        PagePlaceholderView(
            headword: "@Query",
            chapter: "Q",
            kind: "attribute-swiftdata"
        )
    }
}

#Preview {
    PageQuery()
}
