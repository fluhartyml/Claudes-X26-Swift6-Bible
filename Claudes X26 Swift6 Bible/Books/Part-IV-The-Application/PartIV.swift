//
//  PartIV.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartIV: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part IV — The Application")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: Book13_MultiWindowAndNavigationsplitview, Book14_ClipboardDragdropSharesheet, Book15_SwiftdataAndCoredata, Book16_ExtensionsAndPackages, Book17_SwiftChartsAndPdfkit")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartIV()
}
