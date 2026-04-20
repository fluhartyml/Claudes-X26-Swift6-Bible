//
//  PagePrivate.swift
//  Claudes X26 Swift6 Bible
//
//  Page: private  (Chapter P, kind: access-level)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PagePrivate: View {
    var body: some View {
        PagePlaceholderView(
            headword: "private",
            chapter: "P",
            kind: "access-level"
        )
    }
}

#Preview {
    PagePrivate()
}
