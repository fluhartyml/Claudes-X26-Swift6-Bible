//
//  PartII.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartII: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part II — Introduction")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: Book01_IntroducingSwiftAndXcode, Book02_IntroducingSwiftuiViews, Book03_IntroducingScenesAndWindows")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartII()
}
