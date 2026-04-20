# Chapter 10: TextEditor and AttributedString

## TextEditor

`TextEditor` is SwiftUI's multi-line text input. Use it when `TextField` with `axis: .vertical` is not enough.

```swift
@State private var notes = ""

TextEditor(text: $notes)
    .frame(height: 200)
```

### Styling TextEditor

TextEditor has a default background and some built-in padding. You will almost always want to customize it.

```swift
TextEditor(text: $notes)
    .font(.body)
    .foregroundStyle(.primary)
    .scrollContentBackground(.hidden) // remove default background
    .background(.ultraThinMaterial)
    .clipShape(.rect(cornerRadius: 12))
    .frame(minHeight: 100, maxHeight: 300)
```

**Watch out:** Before `.scrollContentBackground(.hidden)` existed, people hacked around the background with `UITextView.appearance()`. Do not do that. Use `.scrollContentBackground(.hidden)` and then apply your own `.background()`.

### Placeholder Text

TextEditor has no built-in placeholder. Overlay one yourself:

```swift
ZStack(alignment: .topLeading) {
    if notes.isEmpty {
        Text("Write your notes here...")
            .foregroundStyle(.tertiary)
            .padding(.top, 8)
            .padding(.leading, 5)
            .allowsHitTesting(false)
    }
    TextEditor(text: $notes)
        .scrollContentBackground(.hidden)
}
```

### Line Limit

```swift
TextEditor(text: $notes)
    .lineLimit(5...10) // constrain vertical growth
```

### Disabling Editing

```swift
TextEditor(text: .constant(readOnlyText))
    // or
TextEditor(text: $notes)
    .disabled(true)
```

### Find and Replace

Enable the system find bar (Cmd+F on Mac, find UI on iPad):

```swift
@State private var isSearchPresented = false

TextEditor(text: $notes)
    .findNavigator(isPresented: $isSearchPresented)
```

Toggle `isSearchPresented` from a button or toolbar item to show/hide find and replace:

```swift
.toolbar {
    Button("Find", systemImage: "magnifyingglass") {
        isSearchPresented.toggle()
    }
}
```

**Watch out:** `.findNavigator` works on TextEditor, List, and Table. It does not work on plain `Text` views.

### Tracking Changes

Use `onChange` to react to text edits:

```swift
TextEditor(text: $notes)
    .onChange(of: notes) { oldValue, newValue in
        wordCount = newValue.split(separator: " ").count
        hasUnsavedChanges = true
    }
```

The two-parameter `onChange` closure (old, new) is the current API. The single-parameter version is deprecated.

---

## Text Selection

Control whether text is selectable:

```swift
Text("Read-only but selectable")
    .textSelection(.enabled)
```

Apply to a container to enable selection for all text inside:

```swift
VStack {
    Text("First line")
    Text("Second line")
    Text("Third line")
}
.textSelection(.enabled)
```

---

## AttributedString

`AttributedString` is Swift's native attributed string type. It replaces most uses of `NSAttributedString` in SwiftUI.

### Creating an AttributedString

```swift
var str = AttributedString("Hello, world")
str.font = .title
str.foregroundColor = .blue
str.underlineStyle = .single

Text(str)
```

### Styling Ranges

```swift
var str = AttributedString("Hello, bold world")
if let range = str.range(of: "bold") {
    str[range].font = .body.bold()
    str[range].foregroundColor = .red
}
Text(str)
```

### Combining AttributedStrings

```swift
var greeting = AttributedString("Hello ")
greeting.font = .headline

var name = AttributedString("Michael")
name.font = .headline
name.foregroundColor = .blue

Text(greeting + name)
```

### Available Attributes

Common attributes you can set on `AttributedString` or its ranges:

| Attribute | Type | Example |
|---|---|---|
| `.font` | `Font` | `.body`, `.title` |
| `.foregroundColor` | `Color` | `.red`, `.blue` |
| `.backgroundColor` | `Color` | `.yellow` |
| `.strikethroughStyle` | `Text.LineStyle` | `.single`, `.double` |
| `.underlineStyle` | `Text.LineStyle` | `.single` |
| `.underlineColor` | `Color` | `.red` |
| `.kern` | `CGFloat` | `2.0` |
| `.tracking` | `CGFloat` | `1.5` |
| `.baselineOffset` | `CGFloat` | `5.0` |
| `.link` | `URL` | `URL(string: "...")` |

---

## Markdown Parsing with AttributedString

`AttributedString` can parse Markdown directly:

```swift
let markdown = "This is **bold**, this is *italic*, and this is a [link](https://example.com)"

if let attributed = try? AttributedString(markdown: markdown) {
    Text(attributed)
}
```

### Parsing Options

```swift
let options = AttributedString.MarkdownParsingOptions(
    interpretedSyntax: .inlineOnlyPreservingWhitespace
)

let str = try? AttributedString(markdown: source, options: options)
```

Interpreted syntax options:
- `.inlineOnlyPreservingWhitespace` -- inline markdown only, keeps whitespace as-is (best for single-line UI text)
- `.full` -- full CommonMark parsing including block elements

### Handling Parse Failures

```swift
do {
    let attributed = try AttributedString(markdown: rawText)
    Text(attributed)
} catch {
    Text(rawText) // fall back to plain text
}
```

**Watch out:** The markdown parser is strict. Malformed markdown throws an error rather than rendering partially. Always have a fallback.

---

## Custom Attributes

You can define your own attributes for domain-specific styling.

### Define the Attribute

```swift
enum HighlightAttribute: CodableAttributedStringKey {
    typealias Value = Bool
    static let name = "highlight"
}

extension AttributeScopes {
    struct AppAttributes: AttributeScope {
        let highlight: HighlightAttribute
    }

    var app: AppAttributes.Type { AppAttributes.self }
}
```

### Use the Custom Attribute

```swift
var str = AttributedString("Important note")
str.highlight = true
```

### Render with Custom Styling

Custom attributes do not auto-style in `Text`. You walk the runs and apply SwiftUI attributes based on your custom ones:

```swift
func styled(_ source: AttributedString) -> AttributedString {
    var result = source
    for run in result.runs {
        if run.highlight == true {
            result[run.range].backgroundColor = .yellow
            result[run.range].font = .body.bold()
        }
    }
    return result
}
```

### Walking Runs

`AttributedString.runs` gives you each contiguous range of uniform attributes:

```swift
for run in attributed.runs {
    print("Text: \(attributed[run.range].characters)")
    print("Font: \(run.font ?? .body)")
    print("---")
}
```

---

## NSAttributedString Bridging

When you need to work with UIKit APIs or older code:

### AttributedString to NSAttributedString

```swift
let modern = AttributedString("Hello")
let legacy = NSAttributedString(modern)
```

### NSAttributedString to AttributedString

```swift
let legacy = NSAttributedString(string: "Hello", attributes: [
    .foregroundColor: UIColor.red,
    .font: UIFont.boldSystemFont(ofSize: 18)
])

let modern = AttributedString(legacy)
Text(modern)
```

**Watch out:** Not all `NSAttributedString` attributes have `AttributedString` equivalents. UIKit-specific attributes like `.paragraphStyle` may not translate cleanly. Test the conversion.

### When You Still Need NSAttributedString

- Core Text rendering
- UIKit text views wrapped in `UIViewRepresentable`
- Specific paragraph style control (line height, alignment, tab stops) not yet in `AttributedString`

---

## Practical Patterns

### Rich Text Display

```swift
struct RichTextView: View {
    let markdown: String

    var body: some View {
        if let attributed = try? AttributedString(markdown: markdown) {
            Text(attributed)
                .font(.body)
                .textSelection(.enabled)
        } else {
            Text(markdown)
                .font(.body)
        }
    }
}
```

### Notes Editor with Word Count

```swift
struct NotesEditor: View {
    @Binding var text: String
    @State private var wordCount = 0
    @State private var showFind = false
    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            TextEditor(text: $text)
                .focused($isFocused)
                .font(.body)
                .scrollContentBackground(.hidden)
                .background(.background.secondary)
                .clipShape(.rect(cornerRadius: 8))
                .findNavigator(isPresented: $showFind)
                .onChange(of: text) { _, newValue in
                    wordCount = newValue.split(separator: " ").count
                }

            HStack {
                Text("\(wordCount) words")
                    .font(.caption)
                    .foregroundStyle(.secondary)

                Spacer()

                Button("Find") { showFind.toggle() }
                    .font(.caption)
            }
        }
    }
}
```

### Highlightable Log Viewer

```swift
func highlightErrors(in log: String) -> AttributedString {
    var result = AttributedString(log)

    let lines = log.components(separatedBy: "\n")
    var position = result.startIndex

    for line in lines {
        let lineEnd = result.index(position, offsetByCharacters: line.count)
        let range = position..<lineEnd

        if line.contains("ERROR") {
            result[range].foregroundColor = .red
            result[range].font = .body.bold()
        } else if line.contains("WARNING") {
            result[range].foregroundColor = .orange
        } else {
            result[range].foregroundColor = .secondary
        }

        // move past the newline
        if lineEnd < result.endIndex {
            position = result.index(lineEnd, offsetByCharacters: 1)
        } else {
            break
        }
    }

    return result
}
```

---

## Quick Reference

| What | How |
|---|---|
| Multi-line input | `TextEditor(text: $binding)` |
| Hide default background | `.scrollContentBackground(.hidden)` |
| Find bar | `.findNavigator(isPresented: $bool)` |
| Track changes | `.onChange(of: text) { old, new in }` |
| Parse markdown | `try AttributedString(markdown: str)` |
| Style a range | `attributed[range].font = .bold()` |
| Walk attributes | `for run in attributed.runs { }` |
| Bridge to NSAttributedString | `NSAttributedString(attributedString)` |
| Enable text selection | `.textSelection(.enabled)` |
