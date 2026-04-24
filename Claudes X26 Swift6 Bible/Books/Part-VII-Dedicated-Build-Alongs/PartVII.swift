//
//  PartVII.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Build-Alongs in this Part.
//  Each Build-Along lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct PartVII: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part VII — Dedicated Build-Alongs")
                .font(.largeTitle.weight(.semibold))
            Text("Build-Alongs in this Part: BuildAlong01_ClaudesWebWrapper, BuildAlong02_QuickNote, BuildAlong03_ClaudesLockBox, BuildAlong04_ClaudesAudioUniverse, BuildAlong05_Outside, BuildAlong06_BodyReadings, BuildAlong07_MyPerson, BuildAlong08_IntelligenceDemo, BuildAlong09_TouchAndMove, BuildAlong10_DragBetweenWindows, BuildAlong11_ReportMaker, BuildAlong12_SwiftUICraft, BuildAlong13_CloudAndErrors, BuildAlong14_TipJar, BuildAlong15_MusicListQuery, BuildAlong16_ChatWithClaude, BuildAlong17_TvOSAmbientDisplay")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    PartVII()
}
