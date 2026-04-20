//
//  PagePrint.swift
//  Claudes X26 Swift6 Bible
//
//  Page: print  (Chapter P, kind: function)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PagePrint: View {
    var body: some View {
        PagePlaceholderView(
            headword: "print",
            chapter: "P",
            kind: "function"
        )
    }
}

#Preview {
    PagePrint()
}
