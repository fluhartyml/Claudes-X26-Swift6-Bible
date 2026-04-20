//
//  AboutView.swift
//  Claudes X26 Swift6 Bible
//
//  Standard About page per feedback_about_page_standard memory.
//  Hero + version + Claude easter egg + contact + portfolio + license.
//
//  About is the brand / credits page. Under the Hood is the Developer
//  Notes. They are deliberately separate views.
//

import SwiftUI

struct AboutView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var easterEggRevealed = false

    private let appName   = "Claude's X26 Swift6 Bible"
    private let appVersion = "1.0 (pre-release)"
    private let developerEmail = "michael.fluharty@mac.com"
    private let portfolioURL = URL(string: "https://fluharty.me")!
    private let githubURL    = URL(string: "https://github.com/fluhartyml")!

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    hero
                    Divider().padding(.horizontal, 40)
                    easterEgg
                    contact
                    portfolio
                    license
                    Spacer(minLength: 40)
                }
                .padding()
                .frame(maxWidth: 560)
                .frame(maxWidth: .infinity)
            }
            .navigationTitle("About")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            #endif
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    // MARK: - Sections

    private var hero: some View {
        VStack(spacing: 10) {
            Image("Hero")
                .resizable()
                .scaledToFit()
                .frame(maxWidth: 240)
                .cornerRadius(12)
                .shadow(radius: 6)
            Text(appName)
                .font(.title.weight(.semibold))
                .multilineTextAlignment(.center)
            Text("Version \(appVersion)")
                .font(.callout)
                .foregroundStyle(.secondary)
        }
    }

    private var easterEgg: some View {
        VStack(spacing: 6) {
            HStack(spacing: 8) {
                Image(systemName: "sparkles")
                    .foregroundStyle(Color.accentColor)
                Text("Engineered with Claude by Anthropic")
                    .font(.callout)
            }
            if easterEggRevealed {
                Text("Thanks for exploring. Every Page in this Bible came out of a conversation.")
                    .font(.footnote)
                    .italic()
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
                    .transition(.opacity.combined(with: .scale))
            }
        }
        .contentShape(Rectangle())
        .onTapGesture {
            withAnimation(.easeInOut) { easterEggRevealed.toggle() }
        }
    }

    private var contact: some View {
        VStack(alignment: .leading, spacing: 4) {
            Label("Contact", systemImage: "envelope")
                .font(.headline)
            Link(developerEmail, destination: URL(string: "mailto:\(developerEmail)")!)
                .font(.body.monospaced())
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var portfolio: some View {
        VStack(alignment: .leading, spacing: 4) {
            Label("Portfolio", systemImage: "link")
                .font(.headline)
            Link(portfolioURL.host() ?? "fluharty.me", destination: portfolioURL)
                .font(.body)
            Link(githubURL.host().map { $0 + (githubURL.path) } ?? "github.com/fluhartyml",
                 destination: githubURL)
                .font(.body)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var license: some View {
        VStack(alignment: .leading, spacing: 4) {
            Label("License", systemImage: "doc.text")
                .font(.headline)
            Text("GPL v3 — Share and share alike, attribution required.")
                .font(.footnote)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

#Preview {
    AboutView()
}
