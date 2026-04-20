//
//  PageString.swift
//  Claudes X26 Swift6 Bible
//
//  Page: String  (Chapter S, kind: type)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageString: View {
    var body: some View {
        PagePlaceholderView(
            headword: "String",
            chapter: "S",
            kind: "type"
        )
    }
}

#Preview {
    PageString()
}
