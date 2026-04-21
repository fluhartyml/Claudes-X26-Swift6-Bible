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
    @StateObject private var webViewBridge = VaultWebView.Bridge()
    @AppStorage("hasSeenOnboarding") private var hasSeenOnboarding = false

    var body: some Scene {
        WindowGroup {
            ZStack {
                ContentView()
                    .environmentObject(vault)
                    .environmentObject(webViewBridge)
                    .preferredColorScheme(.dark)
                    #if os(macOS)
                    .frame(minWidth: 900, minHeight: 720)
                    #endif
                if !hasSeenOnboarding {
                    OnboardingView(onDismiss: { hasSeenOnboarding = true })
                        .transition(.opacity)
                        .zIndex(1)
                }
            }
        }
        #if os(macOS)
        .windowResizability(.contentSize)
        .commands {
            CommandGroup(replacing: .newItem) { }
            CommandGroup(replacing: .appInfo) {
                Button("About Claude's X26 Swift6 Bible") {
                    NotificationCenter.default.post(name: .showAbout, object: nil)
                }
            }
            CommandMenu("Vault") {
                Button("Go to Table of Contents") { vault.goHome() }
                    .keyboardShortcut("h", modifiers: [.command])
                Button("Go to Index") { vault.open("claudex26-index.html") }
                    .keyboardShortcut("a", modifiers: [.command, .shift])
                Button("Go to Roadmap") { vault.open("claudex26-roadmap.html") }
                    .keyboardShortcut("r", modifiers: [.command, .shift])
                Divider()
                Button("Choose Vault Root…") { vault.chooseVaultRoot() }
                    .keyboardShortcut("o", modifiers: [.command])
            }
        }
        #endif
    }
}

extension Notification.Name {
    static let showAbout = Notification.Name("showAbout")
}
