//
//  PageOpen.swift
//  Claudes X26 Swift6 Bible
//
//  Page: open  (Chapter O, kind: access-level)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageOpen: View {
    var body: some View {
        PagePlaceholderView(
            headword: "open",
            chapter: "O",
            kind: "access-level"
        )
    }
}

#Preview {
    PageOpen()
}
