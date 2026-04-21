//
//  PageWarning.swift
//  Claudes X26 Swift6 Bible
//
//  Page: #warning  (Chapter W, kind: directive)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageWarning: View {
    var body: some View {
        PagePlaceholderView(
            headword: "#warning",
            chapter: "W",
            kind: "directive"
        )
    }
}

#Preview {
    PageWarning()
}
