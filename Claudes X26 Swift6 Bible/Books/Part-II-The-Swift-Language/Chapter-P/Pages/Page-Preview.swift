//
//  PagePreview.swift
//  Claudes X26 Swift6 Bible
//
//  Page: #Preview  (Chapter P, kind: macro)
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct PagePreview: View {
    var body: some View {
        PagePlaceholderView(
            headword: "#Preview",
            chapter: "P",
            kind: "macro"
        )
    }
}

#Preview {
    PagePreview()
}
