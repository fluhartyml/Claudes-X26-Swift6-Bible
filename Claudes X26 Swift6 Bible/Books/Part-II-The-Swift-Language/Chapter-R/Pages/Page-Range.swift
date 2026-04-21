//
//  PageRange.swift
//  Claudes X26 Swift6 Bible
//
//  Page: Range  (Chapter R, kind: type)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageRange: View {
    var body: some View {
        PagePlaceholderView(
            headword: "Range",
            chapter: "R",
            kind: "type"
        )
    }
}

#Preview {
    PageRange()
}
