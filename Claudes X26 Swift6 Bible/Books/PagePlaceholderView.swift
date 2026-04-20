//
//  PagePlaceholderView.swift
//  Claudes X26 Swift6 Bible
//
//  Shared view used by every Page file in the Swift Lexicon (Part I).
//  A Page represents one entry (keyword / type / attribute / directive /
//  function / operator / punctuation mark). Each Page's Swift file
//  provides the entry's data to this placeholder.
//
//  Structure per project_lexicon_page_structure memory:
//    Headword · Definition · Swift example · Rosetta Stone
//    (Delphi/Pascal, BASIC, C/C++) · Related · Sources
//

import SwiftUI

struct PagePlaceholderView: View {
    let headword: String
    let chapter: String
    /// What kind of entry this is (keyword / type / attribute / directive / function / operator).
    let kind: String
    let definition: String?
    let swiftExample: String?
    let rosettaDelphi: String?
    let rosettaBASIC: String?
    let rosettaC: String?
    let related: [String]
    let sources: [String]

    init(
        headword: String,
        chapter: String,
        kind: String,
        definition: String? = nil,
        swiftExample: String? = nil,
        rosettaDelphi: String? = nil,
        rosettaBASIC: String? = nil,
        rosettaC: String? = nil,
        related: [String] = [],
        sources: [String] = []
    ) {
        self.headword = headword
        self.chapter = chapter
        self.kind = kind
        self.definition = definition
        self.swiftExample = swiftExample
        self.rosettaDelphi = rosettaDelphi
        self.rosettaBASIC = rosettaBASIC
        self.rosettaC = rosettaC
        self.related = related
        self.sources = sources
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                header
                Divider()
                definitionSection
                exampleSection
                rosettaSection
                relatedSection
                sourcesSection
                Spacer()
            }
            .padding()
            .frame(maxWidth: 800, alignment: .leading)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(headword)
                .font(.system(size: 44, weight: .semibold, design: .monospaced))
            Text("Chapter \(chapter) · \(kind)")
                .font(.callout)
                .foregroundStyle(.secondary)
        }
    }

    private var definitionSection: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Definition")
                .font(.headline)
            Text(definition ?? "— Definition pending. Plain-English description of what this entry does.")
                .font(.body)
                .foregroundStyle(definition == nil ? .secondary : .primary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private var exampleSection: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Swift Example")
                .font(.headline)
            Text(swiftExample ?? "— Code example pending.")
                .font(.body.monospaced())
                .foregroundStyle(swiftExample == nil ? .secondary : .primary)
                .padding(8)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.black.opacity(0.3))
                .cornerRadius(6)
        }
    }

    private var rosettaSection: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("Rosetta Stone")
                .font(.headline)
            Text("What this Swift entry corresponds to in other languages.")
                .font(.caption)
                .foregroundStyle(.secondary)
            rosettaRow("Delphi / Pascal", rosettaDelphi)
            rosettaRow("BASIC", rosettaBASIC)
            rosettaRow("C / C++", rosettaC)
        }
    }

    private func rosettaRow(_ language: String, _ value: String?) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Text(language)
                .font(.callout.weight(.semibold))
                .frame(width: 140, alignment: .leading)
                .foregroundStyle(.secondary)
            Text(value ?? "— pending")
                .font(.callout)
                .foregroundStyle(value == nil ? .secondary : .primary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }

    @ViewBuilder
    private var relatedSection: some View {
        if !related.isEmpty {
            VStack(alignment: .leading, spacing: 4) {
                Text("Related")
                    .font(.headline)
                Text(related.joined(separator: " · "))
                    .font(.body.monospaced())
                    .foregroundStyle(.secondary)
            }
        }
    }

    @ViewBuilder
    private var sourcesSection: some View {
        if !sources.isEmpty {
            VStack(alignment: .leading, spacing: 4) {
                Text("Sources")
                    .font(.headline)
                ForEach(sources, id: \.self) { source in
                    Text("• \(source)")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
        } else {
            Text("— Sources pending (double-cite per BOOK-PARAMETERS.md).")
                .font(.caption)
                .italic()
                .foregroundStyle(.secondary)
                .padding(.top, 8)
        }
    }
}

#Preview {
    PagePlaceholderView(
        headword: "print",
        chapter: "P",
        kind: "function",
        definition: "Writes its argument to standard output. The simplest debugging and I/O function in Swift.",
        swiftExample: "print(\"Hello, world\")",
        rosettaDelphi: "WriteLn(...) in Pascal / Delphi's TForm / Console family.",
        rosettaBASIC: "PRINT \"Hello, world\"",
        rosettaC: "printf(...) or puts(...) in C; std::cout << in C++."
    )
}
