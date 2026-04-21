//
//  PagePublic.swift
//  Claudes X26 Swift6 Bible
//
//  Page: public  (Chapter P, kind: access-level)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PagePublic: View {
    var body: some View {
        PagePlaceholderView(
            headword: "public",
            chapter: "P",
            kind: "access-level"
        )
    }
}

#Preview {
    PagePublic()
}
