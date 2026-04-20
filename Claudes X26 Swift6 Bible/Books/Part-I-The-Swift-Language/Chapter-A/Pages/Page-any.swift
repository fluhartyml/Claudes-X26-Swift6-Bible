//
//  PageAny.swift
//  Claudes X26 Swift6 Bible
//
//  Page: Any  (Chapter A, kind: type)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageAny: View {
    var body: some View {
        PagePlaceholderView(
            headword: "Any",
            chapter: "A",
            kind: "type"
        )
    }
}

#Preview {
    PageAny()
}
