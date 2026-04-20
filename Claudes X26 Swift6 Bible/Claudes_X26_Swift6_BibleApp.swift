//
//  Claudes_X26_Swift6_BibleApp.swift
//  Claudes X26 Swift6 Bible
//
//  Created by Michael Fluharty on 4/20/26.
//

import SwiftUI

@main
struct Claudes_X26_Swift6_BibleApp: App {
    @StateObject private var vault = VaultModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(vault)
                .preferredColorScheme(.dark)
                .frame(minWidth: 900, minHeight: 720)
        }
        #if os(macOS)
        .windowResizability(.contentSize)
        .commands {
            CommandGroup(replacing: .newItem) { }
            CommandMenu("Vault") {
                Button("Go to Table of Contents") { vault.goHome() }
                    .keyboardShortcut("h", modifiers: [.command])
                Button("Go to Atlas") { vault.open("bible-atlas.html") }
                    .keyboardShortcut("a", modifiers: [.command, .shift])
                Button("Go to Roadmap") { vault.open("bible-roadmap.html") }
                    .keyboardShortcut("r", modifiers: [.command, .shift])
                Divider()
                Button("Choose Vault Root…") { vault.chooseVaultRoot() }
                    .keyboardShortcut("o", modifiers: [.command])
            }
        }
        #endif
    }
}
