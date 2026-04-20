//
//  PageRequired.swift
//  Claudes X26 Swift6 Bible
//
//  Page: required  (Chapter R, kind: modifier)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageRequired: View {
    var body: some View {
        PagePlaceholderView(
            headword: "required",
            chapter: "R",
            kind: "modifier"
        )
    }
}

#Preview {
    PageRequired()
}
