//
//  PageBreak.swift
//  Claudes X26 Swift6 Bible
//
//  Page: break  (Chapter B, kind: keyword)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageBreak: View {
    var body: some View {
        PagePlaceholderView(
            headword: "break",
            chapter: "B",
            kind: "keyword"
        )
    }
}

#Preview {
    PageBreak()
}
