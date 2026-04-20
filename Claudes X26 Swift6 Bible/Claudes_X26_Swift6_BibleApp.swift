//
//  Claudes_X26_Swift6_BibleApp.swift
//  Claudes X26 Swift6 Bible
//
//  Created by Michael Fluharty on 4/20/26.
//

import SwiftUI
import SwiftData

@main
struct Claudes_X26_Swift6_BibleApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Item.self,
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(sharedModelContainer)
    }
}
