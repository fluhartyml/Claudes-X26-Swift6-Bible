//
//  PageSelector.swift
//  Claudes X26 Swift6 Bible
//
//  Page: #selector  (Chapter S, kind: directive)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageSelector: View {
    var body: some View {
        PagePlaceholderView(
            headword: "#selector",
            chapter: "S",
            kind: "directive"
        )
    }
}

#Preview {
    PageSelector()
}
