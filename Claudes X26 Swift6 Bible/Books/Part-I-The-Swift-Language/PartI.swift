//
//  PartI.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartI: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part I — The Swift Language")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: ChapterA, ChapterB, ChapterC, ChapterD, ChapterE, ChapterF, ChapterG, ChapterH, ChapterI, ChapterJ, ChapterK, ChapterL, ChapterM, ChapterN, ChapterO, ChapterP, ChapterQ, ChapterR, ChapterS, ChapterT, ChapterU, ChapterV, ChapterW, ChapterX, ChapterY, ChapterZ")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartI()
}
