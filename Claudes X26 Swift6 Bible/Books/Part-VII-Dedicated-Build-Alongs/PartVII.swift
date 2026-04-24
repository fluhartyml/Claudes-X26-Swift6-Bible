//
//  PartVII.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists all app entries in this Part — both
//  Build-Alongs (how to build the primary sample apps) and Source Tours
//  (installed production apps readers browse at scale).
//

import SwiftUI

struct PartVII: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Part VII — The Apps")
                .font(.largeTitle.weight(.semibold))
            Text("Entries in this Part: BuildAlong01_ClaudesWebWrapper, BuildAlong02_QuickNote, BuildAlong03_ClaudesLockBox, BuildAlong04_ClaudesAudioUniverse, BuildAlong05_Outside, BuildAlong06_BodyReadings, BuildAlong07_MyPerson, BuildAlong08_IntelligenceDemo, BuildAlong09_TouchAndMove, BuildAlong10_DragBetweenWindows, BuildAlong11_ReportMaker, BuildAlong12_SwiftUICraft, BuildAlong13_CloudAndErrors, BuildAlong14_TipJar, BuildAlong15_MusicListQuery, BuildAlong16_ChatWithClaude, BuildAlong17_TvOSAmbientDisplay, SourceTour18_CryoTunesPlayer, SourceTour19_TallyMatrixClock, SourceTour20_SnapAndScanKeeper, SourceTour21_CryoPlaylistManager, SourceTour22_NightGardLibraryCommander, SourceTour23_NightGardCommander, SourceTour24_NightGardDDNS, SourceTour25_ClaudesX26Swift6Bible")
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
