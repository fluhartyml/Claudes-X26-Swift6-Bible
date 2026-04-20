//
//  PartVI.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartVI: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part VI — The Modern Toolchain")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: Book21_GitAndGithub, Book22_AiChatbotIntegration")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartVI()
}
