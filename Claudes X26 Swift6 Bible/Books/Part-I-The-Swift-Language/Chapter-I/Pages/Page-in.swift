//
//  PageIn.swift
//  Claudes X26 Swift6 Bible
//
//  Page: in  (Chapter I, kind: keyword)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageIn: View {
    var body: some View {
        PagePlaceholderView(
            headword: "in",
            chapter: "I",
            kind: "keyword"
        )
    }
}

#Preview {
    PageIn()
}
