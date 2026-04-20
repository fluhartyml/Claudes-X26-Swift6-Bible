//
//  OnboardingView.swift
//  Claudes X26 Swift6 Bible
//
//  First-launch welcome. Shown once; tracked via UserDefaults key
//  "hasSeenOnboarding". After dismissal, the app opens to the last
//  page the reader was on (or the table of contents on first run).
//

import SwiftUI

struct OnboardingView: View {
    let onDismiss: () -> Void

    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            Image("Hero")
                .resizable()
                .scaledToFit()
                .frame(maxWidth: 320)
                .cornerRadius(14)
                .shadow(radius: 12)
            VStack(spacing: 8) {
                Text("Claude's X26 Swift6 Bible")
                    .font(.largeTitle.weight(.semibold))
                    .multilineTextAlignment(.center)
                Text("A living reference for Swift 6, SwiftUI, and Xcode 26.")
                    .font(.title3)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 32)
            }
            Spacer()
            Button {
                onDismiss()
            } label: {
                Text("Begin Reading")
                    .font(.headline)
                    .frame(maxWidth: 260)
                    .padding(.vertical, 4)
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            Spacer(minLength: 20)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.black.ignoresSafeArea())
    }
}

#Preview {
    OnboardingView(onDismiss: { })
        .preferredColorScheme(.dark)
}
