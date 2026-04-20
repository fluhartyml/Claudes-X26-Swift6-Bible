//
//  PartIII.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartIII: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part III — The User Interface")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: Book04_GesturesAndInput, Book05_MenusAndNavigation, Book06_ControlsButtonsTogglesPickers, Book07_ToolbarsAndTabViews, Book08_ListsGridsAndForeach, Book09_TextAndTextfield, Book10_TexteditorAndAttributedstring, Book11_FilemanagerAndDocuments, Book12_SheetsAlertsAndConfirmations")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartIII()
}
