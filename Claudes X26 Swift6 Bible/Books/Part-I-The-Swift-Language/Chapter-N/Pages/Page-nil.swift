//
//  PageNil.swift
//  Claudes X26 Swift6 Bible
//
//  Page: nil  (Chapter N, kind: literal)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageNil: View {
    var body: some View {
        PagePlaceholderView(
            headword: "nil",
            chapter: "N",
            kind: "literal"
        )
    }
}

#Preview {
    PageNil()
}
