//
//  PageImport.swift
//  Claudes X26 Swift6 Bible
//
//  Page: import  (Chapter I, kind: keyword)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PageImport: View {
    var body: some View {
        PagePlaceholderView(
            headword: "import",
            chapter: "I",
            kind: "keyword"
        )
    }
}

#Preview {
    PageImport()
}
