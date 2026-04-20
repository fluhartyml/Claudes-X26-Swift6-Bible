# Chapter 2: Introducing SwiftUI Views

**Claude's Swift Bible 26** -- Part I: Introduction

---

## What SwiftUI Is

SwiftUI is Apple's declarative UI framework. You describe *what* you want the interface to look like, and SwiftUI figures out *how* to render it and *when* to update it.

It shipped in 2019 and has matured significantly. As of Swift 6 / Xcode 26, SwiftUI is the primary way to build Apple apps. UIKit still exists and works, but new projects should start with SwiftUI.

### Declarative vs. Imperative

**UIKit (imperative):** You create a button, configure it, add it to a view, write code to handle layout changes, and manually update it when data changes.

```swift
// UIKit way -- you manage everything yourself
let label = UILabel()
label.text = "Score: 0"
label.font = .systemFont(ofSize: 18)
view.addSubview(label)
// ...later, when score changes:
label.text = "Score: \(newScore)"
```

**SwiftUI (declarative):** You describe the view once. SwiftUI watches your data and re-renders automatically when it changes.

```swift
// SwiftUI way -- describe it, SwiftUI handles the rest
Text("Score: \(score)")
    .font(.system(size: 18))
```

When `score` changes, SwiftUI updates the `Text` automatically. You never manually set the text.

---

## The View Protocol

Every piece of UI in SwiftUI conforms to the `View` protocol. The protocol has one requirement: a computed property called `body` that returns some other `View`.

```swift
struct ScoreCard: View {
    var body: some View {
        Text("Hello, Michael")
            .font(.system(size: 18, weight: .bold))
    }
}
```

That is a complete SwiftUI view. A few things to notice:

- **struct, not class.** SwiftUI views are value types. They are lightweight and frequently recreated. Do not put heavy logic in a view's initializer.
- **some View.** This is an "opaque return type." It means "I return a specific View type, but I am not telling you which one." The compiler figures it out.
- **body is computed.** It has no stored value. SwiftUI calls it whenever it needs to know what this view looks like right now.

### Watch Out For

- The `body` property must return exactly **one** root view. If you need multiple views, wrap them in a container (`VStack`, `HStack`, `ZStack`, `Group`).
- Do not put side effects (network calls, file writes, print statements) inside `body`. It can be called many times. Use `.onAppear`, `.task`, or event handlers instead.

---

## View Composition

SwiftUI is built on composition. You build small views and combine them into larger ones.

```swift
struct PlayerRow: View {
    let name: String
    let score: Int

    var body: some View {
        HStack {
            Text(name)
                .font(.system(size: 18))
            Spacer()
            Text("\(score)")
                .font(.system(size: 18, weight: .bold))
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

struct Scoreboard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            PlayerRow(name: "Michael", score: 42)
            PlayerRow(name: "Claude", score: 38)
        }
        .padding()
    }
}
```

There is no limit to nesting depth. Break views into separate structs whenever a `body` gets hard to read -- generally past 30-40 lines.

---

## Layout Containers

SwiftUI provides three primary layout containers:

### HStack -- Horizontal

```swift
HStack(spacing: 12) {
    Image(systemName: "star.fill")
    Text("Favorites")
        .font(.system(size: 18))
}
```

### VStack -- Vertical

```swift
VStack(alignment: .leading, spacing: 8) {
    Text("Title")
        .font(.system(size: 24, weight: .bold))
    Text("Subtitle")
        .font(.system(size: 18))
        .foregroundStyle(.secondary)
}
```

### ZStack -- Overlapping (Z-axis)

```swift
ZStack {
    Color.blue
    Text("Overlay")
        .font(.system(size: 18))
        .foregroundStyle(.white)
}
```

Later children in a ZStack render on top of earlier ones.

### Grid -- Two-Dimensional Layout (iOS 16+)

```swift
Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
    GridRow {
        Text("Name")
            .font(.system(size: 18, weight: .bold))
        Text("Score")
            .font(.system(size: 18, weight: .bold))
    }
    GridRow {
        Text("Michael")
            .font(.system(size: 18))
        Text("42")
            .font(.system(size: 18))
    }
}
```

### Watch Out For

- `VStack` and `HStack` have a **10-child limit** in their `@ViewBuilder` closure. If you need more, wrap groups in `Group {}` or use `ForEach`.
- `Spacer()` in an `HStack` pushes content to the edges. It is the most common way to achieve "left-align this, right-align that" layouts.

---

## @State -- View-Local Mutable Data

By default, view structs are immutable. If you need a value that changes and triggers re-rendering, mark it `@State`.

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 16) {
            Text("Count: \(count)")
                .font(.system(size: 24, weight: .bold))

            Button("Add One") {
                count += 1
            }
            .font(.system(size: 18))
        }
    }
}
```

When `count` changes, SwiftUI re-evaluates `body` and updates only the parts that changed (the `Text` in this case).

### Rules of @State

1. Always mark `@State` properties `private`. They belong to this view and no one else.
2. `@State` survives view re-creation. SwiftUI stores the actual value separately from the struct.
3. Initialize `@State` with a default value. Do not try to set it from outside the view (use `@Binding` or `@Observable` for that).

### Watch Out For

- `@State` is for **simple, view-local** values: a toggle boolean, a text field string, a counter. If multiple views need to share the same data, use `@Observable` (see below).
- Mutating `@State` inside `body` (outside of a closure like a button action) causes an infinite loop. SwiftUI re-evaluates `body`, which changes state, which re-evaluates `body`, forever.

---

## @Binding -- Two-Way Connection

A `@Binding` creates a two-way connection to someone else's `@State`. The child view can read and write the value, and changes flow back to the owner.

```swift
struct ToggleRow: View {
    let label: String
    @Binding var isOn: Bool

    var body: some View {
        Toggle(label, isOn: $isOn)
            .font(.system(size: 18))
    }
}

struct SettingsView: View {
    @State private var darkMode = false
    @State private var notifications = true

    var body: some View {
        VStack(spacing: 12) {
            ToggleRow(label: "Dark Mode", isOn: $darkMode)
            ToggleRow(label: "Notifications", isOn: $notifications)
        }
        .padding()
    }
}
```

The `$` prefix creates a binding from a `@State` property. `$darkMode` is a `Binding<Bool>` that reads and writes the underlying `darkMode` state.

### Watch Out For

- You cannot create a `@Binding` out of thin air. It must connect to a source of truth (`@State`, `@Observable` property, etc.).
- For previews and testing, use `.constant()`: `ToggleRow(label: "Test", isOn: .constant(true))`.

---

## @Observable -- Shared Data Model (iOS 17+)

`@Observable` is the modern way to share data across multiple views. It replaces the older `ObservableObject` / `@Published` / `@ObservedObject` pattern.

```swift
@Observable
class GameState {
    var score = 0
    var playerName = "Michael"
    var isPlaying = false
}
```

That is it. No `@Published` wrappers. The `@Observable` macro automatically tracks which properties each view reads, and only re-renders views that actually use changed properties.

### Using @Observable in Views

```swift
struct GameView: View {
    var game: GameState

    var body: some View {
        VStack(spacing: 16) {
            Text("\(game.playerName)'s Score: \(game.score)")
                .font(.system(size: 24, weight: .bold))

            Button("Score Point") {
                game.score += 1
            }
            .font(.system(size: 18))
        }
    }
}

struct ContentView: View {
    @State private var game = GameState()

    var body: some View {
        GameView(game: game)
    }
}
```

The top-level view owns the `GameState` as `@State`. Child views receive it as a plain property. SwiftUI tracks dependencies automatically.

### @Environment for Deep Passing

If you need to pass an `@Observable` object deep into the view hierarchy without threading it through every intermediate view:

```swift
// In the top-level view:
GameView()
    .environment(game)

// In any descendant view:
struct DeepChildView: View {
    @Environment(GameState.self) private var game

    var body: some View {
        Text("Score: \(game.score)")
            .font(.system(size: 18))
    }
}
```

### Watch Out For

- `@Observable` requires iOS 17 / macOS 14 minimum. If you need to support older OS versions, use `ObservableObject` with `@Published` properties.
- `@Observable` classes are reference types (classes, not structs). Multiple views holding the same instance see the same data. This is the point.
- If an `@Observable` property changes but no view reads it, no re-render happens. This is efficient and intentional.

---

## View Modifiers

View modifiers are methods you chain onto views to change their appearance or behavior. Each modifier returns a new view wrapping the original.

```swift
Text("Important Notice")
    .font(.system(size: 20, weight: .bold))
    .foregroundStyle(.red)
    .padding()
    .background(.yellow.opacity(0.3))
    .clipShape(RoundedRectangle(cornerRadius: 8))
```

### Order Matters

Modifiers apply from inside out. This catches people constantly.

```swift
// Padding THEN background: background includes the padding
Text("Hello")
    .padding()
    .background(.blue)

// Background THEN padding: background is tight to the text, padding is outside
Text("Hello")
    .background(.blue)
    .padding()
```

These produce visually different results. The first has a blue box with padding inside. The second has a tight blue background with empty space around it.

### Common Modifiers

| Modifier | What It Does |
|----------|-------------|
| `.font(.system(size: 18))` | Sets font size (use 18+ for accessibility) |
| `.foregroundStyle(.primary)` | Text/icon color |
| `.padding()` | Adds space around the view |
| `.padding(.horizontal, 16)` | Adds space on specific edges |
| `.frame(width:height:alignment:)` | Constrains or expands the view's size |
| `.background(...)` | Puts something behind the view |
| `.overlay(...)` | Puts something on top of the view |
| `.clipShape(...)` | Clips to a shape (circle, rounded rect) |
| `.opacity(0.5)` | Transparency |
| `.hidden()` | Hides the view (still takes up space) |
| `.disabled(true)` | Grays out and disables interaction |
| `.accessibilityLabel("...")` | VoiceOver label |

### Writing Custom Modifiers

For reusable styling, create a `ViewModifier`:

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}

// Usage:
Text("Hello")
    .font(.system(size: 18))
    .cardStyle()
```

---

## Previews

SwiftUI Previews let you see your views in Xcode without running the app. They update in real-time as you type.

```swift
#Preview {
    ContentView()
}

// Named preview:
#Preview("Dark Mode") {
    ContentView()
        .preferredColorScheme(.dark)
}

// Multiple previews:
#Preview("Large Text") {
    ContentView()
        .environment(\.dynamicTypeSize, .accessibility3)
}
```

### Preview Tips

- Wrap previews in a `NavigationStack` if your view expects to be inside one.
- Pass mock data to previews, not real network calls.
- If previews refuse to load, try: Resume (click the "Resume" button), clean build (Cmd+Shift+K), or restart Xcode.
- Previews run in Debug configuration. They can be slow with complex views.

### Watch Out For

- Previews crash if your view requires an `@Environment` value that is not provided. Always supply required environment values in your preview.
- Previews do not support all device features (camera, Bluetooth, etc.).
- If previews show "Cannot preview in this file," there is usually a compile error somewhere. Check the build log.

---

## The View Hierarchy

SwiftUI builds a tree of views. Understanding this tree helps you reason about layout, updates, and performance.

```
App
  WindowGroup
    ContentView
      NavigationStack
        VStack
          Text("Title")
          List
            ForEach
              PlayerRow
                HStack
                  Text(name)
                  Spacer
                  Text(score)
```

### How Updates Flow

1. A `@State` or `@Observable` property changes
2. SwiftUI identifies which views read that property
3. Those views have their `body` re-evaluated
4. SwiftUI diffs the old and new view trees
5. Only the actual differences are rendered on screen

This is why you should keep `body` cheap. It may be called frequently, but SwiftUI only does real rendering work when the output actually changes.

### Identity and Lifetime

SwiftUI uses **structural identity** (position in the view tree) to track views across updates. If you use `ForEach` with an `id` parameter, that `id` is how SwiftUI knows which item is which.

```swift
ForEach(players, id: \.name) { player in
    PlayerRow(player: player)
}
```

If two views swap positions but keep their IDs, SwiftUI animates the swap rather than destroying and recreating them.

### Watch Out For

- Using `ForEach(0..<array.count)` instead of `ForEach(array, id: \.self)` (or a proper `Identifiable` conformance) breaks animations and can cause visual glitches. Always give SwiftUI stable identifiers.
- Deeply nested view hierarchies are fine for readability but can slow down the compiler. If Xcode says "expression too complex," break the view into smaller sub-views.

---

## UIKit Interop

Sometimes you need a UIKit view in SwiftUI (for features SwiftUI does not cover yet). Use `UIViewRepresentable`:

```swift
import UIKit
import SwiftUI

struct ActivityIndicator: UIViewRepresentable {
    func makeUIView(context: Context) -> UIActivityIndicatorView {
        let indicator = UIActivityIndicatorView(style: .large)
        indicator.startAnimating()
        return indicator
    }

    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        // Update the view if needed when SwiftUI state changes
    }
}
```

There is also `UIViewControllerRepresentable` for wrapping full UIKit view controllers. Use these as bridges, not as a primary development strategy.

---

## Accessibility Essentials

SwiftUI has strong accessibility support built in, but you need to be intentional about it.

### Font Sizing

Use `Dynamic Type` sizes or explicit minimums. Michael's 18pt minimum means:

```swift
// Good -- explicit minimum size
Text("Readable text")
    .font(.system(size: 18))

// Also good -- use a text style that scales
Text("Readable text")
    .font(.title3) // 20pt default, scales with Dynamic Type
```

Font sizes below `.title3` (which is 20pt) drop below 18pt at default Dynamic Type. The safe "always 18pt+" text styles are: `.largeTitle`, `.title`, `.title2`, `.title3`.

If you use `.body` (17pt default), it drops below 18pt at default settings. Either use `.system(size: 18)` explicitly or use `.title3` and up.

### Accessibility Modifiers

```swift
Image(systemName: "star.fill")
    .accessibilityLabel("Favorite")

// Group related content for VoiceOver:
HStack {
    Text("Score:")
    Text("\(score)")
}
.accessibilityElement(children: .combine)

// Hide decorative elements:
Image("decorative-line")
    .accessibilityHidden(true)
```

### Watch Out For

- Do not use `.font(.caption)` or `.font(.footnote)` for anything the user actually needs to read. They are 12pt and 13pt respectively -- too small.
- Always test with VoiceOver at least once before shipping. Simulator > Settings > Accessibility > VoiceOver.
- Color alone should never be the only way to convey information. Pair it with text, icons, or shapes.

---

## Practical Tips

1. **Start with the data, then build the view.** Define your model types first, then write the views that display them. SwiftUI works best when your data flow is clear.

2. **One source of truth.** Every piece of data should have exactly one owner. Other views get a binding or a reference, never a copy they also mutate.

3. **Extract early, extract often.** When a view body gets past 30 lines, pull part of it into a separate struct. This is free in SwiftUI -- small structs cost nothing.

4. **Use `@Observable` for shared state, `@State` for local state.** If only one view cares about a value, it is `@State`. If multiple views share it, it is `@Observable`.

5. **Previews are your rapid feedback loop.** Set up multiple previews (light mode, dark mode, large text) so you catch layout issues without running the app.

6. **When something looks wrong, check modifier order.** Swapping `.padding()` and `.background()` changes the result. Read modifiers bottom-to-top to understand layering.

---

*Claude's Swift Bible 26 -- Chapter 2*
*Written by Claude for Michael Fluharty. Swift 6, Xcode 26.*
