# Chapter 2: Introducing SwiftUI Views

*Claude's Xcode 26 Swift Bible — Part I: Introduction*

---

## 1. What SwiftUI Is

1.1 SwiftUI is how you build the stuff people see and touch in your app. It's Apple's UI framework — shipped in 2019, and as of Xcode 26 it's the primary way to build apps for every Apple platform. UIKit still exists and works, but new projects should start here.

_1.2 The big idea is **declarative programming**. Instead of telling the computer step by step how to build a screen, you describe what the screen should look like and SwiftUI handles the rest — figuratively speaking, it translates your description into the actual drawing and updating behind the scenes. When your data changes, SwiftUI automatically updates only the parts of the screen that need to change. You don't manually refresh anything.

1.3 **The old way (UIKit — imperative):**

```swift
// UIKit: you create it, configure it, place it, and update it yourself
let label = UILabel()
label.text = "Score: 0"
label.font = .systemFont(ofSize: 18)
view.addSubview(label)
// ...later, when the score changes:
label.text = "Score: \(newScore)"
```

1.4 **The new way (SwiftUI — declarative):**

```swift
// SwiftUI: describe it once, it updates itself
Text("Score: \(score)")
    .font(.system(size: 18))
```

1.5 When `score` changes, SwiftUI updates the text automatically. You never touch it again. That's the whole philosophy — describe the end result, not the steps to get there.

---

## 2. The View Protocol

2.1 Every piece of UI in SwiftUI is a **View**. A button is a View. A text label is a View. A whole screen is a View made of smaller Views. It's Views all the way down.

_2.2 To make your own View, you create a **struct** <<Glossary: Struct>> — a lightweight container that holds data and behavior together as a single unit. The struct conforms to the **View protocol** <<Glossary: View Protocol>>, which is SwiftUI's way of saying "this thing can be drawn on screen." The only requirement is a computed property called `body` that returns what this View looks like:

```swift
struct ScoreCard: View {
    var body: some View {
        Text("Hello, Michael")
            .font(.system(size: 18, weight: .bold))
    }
}
```

2.3 That's a complete SwiftUI view. A few things to notice:

_2.4 **It's a struct, not a class.** A struct <<Glossary: Struct>> and a class <<Glossary: Class>> are both containers for data and behavior, but they work differently under the hood. A struct is a **value type** — when you pass it around, Swift makes a copy. A class is a **reference type** — when you pass it around, everyone shares the same object. SwiftUI uses structs for views because they're cheap to create, cheap to copy, and cheap to throw away. SwiftUI creates and destroys views constantly as your screen updates — that's normal and by design. Classes carry more overhead and introduce shared-state complexity that views don't need. Don't put heavy work (network calls, database reads) in a view's initializer — it runs every time SwiftUI recreates the view.

2.5 **`some View` is an opaque return type.** It means "I'm returning a specific kind of View, but I'm not spelling out the exact type." The compiler figures it out. You don't need to worry about what type `body` actually returns — just put views in there.

_2.6 **`body` is computed, not stored.** "Computed" here doesn't mean math — it means the property runs code every time you access it instead of holding a fixed value. A stored property is like a box with a value sitting in it (`var name = "Michael"`). A computed property is like asking a question — it runs fresh every time someone reads it. SwiftUI doesn't store your view layout once and reuse it. Every time something changes, it asks `body` "what should this look like right now?" and `body` runs again to answer. This can happen many times, so keep `body` lightweight — no network calls, no heavy calculations. <<Glossary: Computed Property>>

2.7 **Watch out:** The `body` property must return exactly one root view. If you need multiple things on screen, wrap them in a container like `VStack`, `HStack`, or `ZStack` (covered in section 4). Don't put side effects inside `body` — no network calls, no file writes, no print statements. Use `.onAppear`, `.task`, or button actions for that kind of work.

---

## 3. View Composition

3.1 SwiftUI is built on **composition** — you build small views and snap them together into bigger ones. Like LEGO blocks.

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

3.2 `PlayerRow` is a small view. `Scoreboard` uses two of them. You can nest as deep as you want. When a view's `body` gets hard to read — generally past 30-40 lines — break part of it into its own struct. This is free in SwiftUI. Small structs cost nothing.

---

## 4. Layout Containers

4.1 SwiftUI gives you three primary containers for arranging views on screen:

4.2 **HStack — Horizontal.** Lines things up side by side, left to right.

```swift
HStack(spacing: 12) {
    Image(systemName: "star.fill")
    Text("Favorites")
        .font(.system(size: 18))
}
```

4.3 **VStack — Vertical.** Stacks things top to bottom.

```swift
VStack(alignment: .leading, spacing: 8) {
    Text("Title")
        .font(.system(size: 24, weight: .bold))
    Text("Subtitle")
        .font(.system(size: 18))
        .foregroundStyle(.secondary)
}
```

4.4 **ZStack — Overlapping.** Layers things on top of each other along the Z-axis. The last item in the list renders on top.

```swift
ZStack {
    Color.blue
    Text("Overlay")
        .font(.system(size: 18))
        .foregroundStyle(.white)
}
```

4.5 **Grid — Two-Dimensional Layout (iOS 16+).** Rows and columns, like a table without the table.

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

4.6 **Watch out:** `VStack` and `HStack` have a 10-child limit in their closure. If you need more than 10 items, wrap groups in `Group {}` or use `ForEach`. `Spacer()` inside an `HStack` pushes content to the edges — that's how you left-align one thing and right-align another.

---

## 5. @State — View-Local Mutable Data

5.1 View structs are immutable by default — you can't change their properties. If you need a value that changes and triggers the screen to update, mark it `@State`.

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

5.2 When `count` changes, SwiftUI re-evaluates `body` and updates only the parts that changed — in this case, the Text. You don't tell it to refresh. It just knows.

5.3 **Rules of @State:**
1) Always mark `@State` properties `private`. They belong to this view and nobody else.
2) `@State` survives view re-creation. SwiftUI stores the actual value separately from the struct.
3) Initialize `@State` with a default value. Don't try to set it from outside the view — use `@Binding` or `@Observable` for that.

5.4 **Watch out:** `@State` is for simple, view-local values — a toggle boolean, a text field string, a counter. If multiple views need to share the same data, use `@Observable` (section 7). And never mutate `@State` directly inside `body` outside of a closure — that causes an infinite loop. SwiftUI re-evaluates `body`, which changes state, which re-evaluates `body`, forever.

---

## 6. @Binding — Two-Way Connection

6.1 A `@Binding` creates a two-way connection to someone else's `@State`. The child view can read and write the value, and changes flow back to the owner.

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

6.2 The `$` prefix creates a binding from a `@State` property. `$darkMode` is a `Binding<Bool>` that reads and writes the underlying `darkMode` state. The child view doesn't own the data — it's just borrowing it.

6.3 **Watch out:** You can't create a `@Binding` out of thin air. It must connect to a source of truth — a `@State`, an `@Observable` property, or something that actually holds the data. For previews and testing, use `.constant()`: `ToggleRow(label: "Test", isOn: .constant(true))`.

---

## 7. @Observable — Shared Data Model (iOS 17+)

7.1 When multiple views need to share the same data, `@Observable` is the modern way to do it. It's a macro you put on a class, and SwiftUI automatically tracks which properties each view reads. Only the views that actually use a changed property get re-rendered.

```swift
@Observable
class GameState {
    var score = 0
    var playerName = "Michael"
    var isPlaying = false
}
```

7.2 That's it. No `@Published` wrappers, no `ObservableObject` protocol. The `@Observable` macro handles everything.

7.3 **Using it in views:**

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

7.4 The top-level view owns the `GameState` as `@State`. Child views receive it as a plain property. SwiftUI tracks what each view reads automatically.

7.5 **@Environment for passing data deep.** If you need an `@Observable` object several layers down without threading it through every intermediate view:

```swift
// At the top:
GameView()
    .environment(game)

// In any descendant, no matter how deep:
struct DeepChildView: View {
    @Environment(GameState.self) private var game

    var body: some View {
        Text("Score: \(game.score)")
            .font(.system(size: 18))
    }
}
```

7.6 **Watch out:** `@Observable` requires iOS 17 / macOS 14 minimum. If your deployment target is older, you need the older `ObservableObject` with `@Published` properties pattern. Also, `@Observable` only works on classes (reference types), not structs — multiple views holding the same instance see the same data. That's the point.

---

## 8. View Modifiers

8.1 Modifiers are methods you chain onto a view to change how it looks or behaves. Each modifier wraps the view and returns a new one.

```swift
Text("Important Notice")
    .font(.system(size: 20, weight: .bold))
    .foregroundStyle(.red)
    .padding()
    .background(.yellow.opacity(0.3))
    .clipShape(RoundedRectangle(cornerRadius: 8))
```

8.2 **Order matters.** This is the single most common source of confusion in SwiftUI. Modifiers apply from inside out.

```swift
// Padding THEN background: the blue box includes the padding
Text("Hello")
    .padding()
    .background(.blue)

// Background THEN padding: the blue is tight to the text, padding is empty space outside
Text("Hello")
    .background(.blue)
    .padding()
```

8.3 These look completely different on screen. If something looks wrong, check your modifier order. Read modifiers bottom-to-top to understand the layering.

8.4 **Common modifiers:**
- `.font(.system(size: 18))` — sets font size (18pt minimum for readability)
- `.foregroundStyle(.primary)` — text/icon color
- `.padding()` — adds space around the view
- `.padding(.horizontal, 16)` — adds space on specific edges
- `.frame(width:height:alignment:)` — constrains or expands the view's size
- `.background(...)` — puts something behind the view
- `.overlay(...)` — puts something on top of the view
- `.clipShape(...)` — clips to a shape (circle, rounded rectangle)
- `.opacity(0.5)` — transparency
- `.hidden()` — hides the view but it still takes up space
- `.disabled(true)` — grays out and disables interaction
- `.accessibilityLabel("...")` — VoiceOver label

8.5 **Custom modifiers.** If you find yourself applying the same chain of modifiers in multiple places, make a reusable `ViewModifier`:

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

## 9. Previews

9.1 SwiftUI Previews let you see your views in Xcode without building and running the app. They update as you type — like a live mirror of your code.

```swift
#Preview {
    ContentView()
}

// Named preview with dark mode:
#Preview("Dark Mode") {
    ContentView()
        .preferredColorScheme(.dark)
}

// Large text for accessibility testing:
#Preview("Large Text") {
    ContentView()
        .environment(\.dynamicTypeSize, .accessibility3)
}
```

9.2 **Tips:**
- Wrap previews in a `NavigationStack` if your view expects to be inside one
- Pass mock data, not real network calls
- If previews won't load, try: click Resume, clean build (Cmd+Shift+K), or restart Xcode
- Set up multiple previews (light mode, dark mode, large text) so you catch layout issues without running the app

9.3 **Watch out:** Previews crash if your view requires an `@Environment` value that you didn't provide in the preview. Always supply required environment values. If previews show "Cannot preview in this file," there's usually a compile error somewhere — check the build log.

---

## 10. The View Hierarchy

10.1 SwiftUI builds a tree of views. Understanding this tree helps you think about layout, updates, and performance.

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

10.2 **How updates flow:**
1) A `@State` or `@Observable` property changes
2) SwiftUI identifies which views read that property
3) Those views have their `body` re-evaluated
4) SwiftUI diffs the old tree against the new tree
5) Only the actual differences are rendered on screen

10.3 This is why `body` should be cheap to run. It gets called often, but SwiftUI only does real rendering work when the output actually changes.

10.4 **Identity and lifetime.** SwiftUI uses structural identity — a view's position in the tree — to track it across updates. When you use `ForEach`, give it a stable identifier so SwiftUI knows which item is which:

```swift
ForEach(players, id: \.name) { player in
    PlayerRow(player: player)
}
```

10.5 **Watch out:** Using `ForEach(0..<array.count)` instead of `ForEach(array, id: \.self)` or proper `Identifiable` conformance breaks animations and causes visual glitches. Always give SwiftUI stable identifiers. And if Xcode says "expression too complex to solve in reasonable time," break the view into smaller sub-views.

---

## 11. UIKit Interop

11.1 Sometimes SwiftUI doesn't have a native equivalent for something UIKit can do. When that happens, you bridge UIKit views into SwiftUI using `UIViewRepresentable`:

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
        // Update the view if SwiftUI state changes
    }
}
```

11.2 There's also `UIViewControllerRepresentable` for wrapping entire UIKit view controllers. Use these as bridges when you need them, not as your main development approach. SwiftUI covers most things now.

---

## 12. Accessibility

12.1 SwiftUI has strong accessibility support built in, but you need to be intentional about it.

12.2 **Font sizing.** The book's 18pt minimum means using `.system(size: 18)` or a text style that's 18pt or larger. The safe text styles that stay at or above 18pt at default Dynamic Type are: `.largeTitle`, `.title`, `.title2`, `.title3` (20pt). The `.body` style is 17pt — one point short. Either use an explicit size or stick to `.title3` and up.

12.3 **Accessibility modifiers:**

```swift
// Give VoiceOver a label for an icon:
Image(systemName: "star.fill")
    .accessibilityLabel("Favorite")

// Combine related content so VoiceOver reads it as one item:
HStack {
    Text("Score:")
    Text("\(score)")
}
.accessibilityElement(children: .combine)

// Hide purely decorative elements from VoiceOver:
Image("decorative-line")
    .accessibilityHidden(true)
```

12.4 **Watch out:** Don't use `.font(.caption)` or `.font(.footnote)` for anything the user needs to read — they're 12pt and 13pt. Always test with VoiceOver at least once before shipping (Simulator > Settings > Accessibility > VoiceOver). And never use color alone to convey information — pair it with text, icons, or shapes.

---

## 13. Tips

13.1 **Start with the data, then build the view.** Define your model types first, then write the views that display them. SwiftUI works best when your data flow is clear.

13.2 **One source of truth.** Every piece of data should have exactly one owner. Other views get a binding or a reference, never a separate copy they also mutate.

13.3 **Extract early, extract often.** When a view body gets past 30 lines, pull part of it into a separate struct. Small structs cost nothing in SwiftUI.

13.4 **Use `@Observable` for shared state, `@State` for local state.** If only one view cares about a value, it's `@State`. If multiple views share it, it's `@Observable`.

13.5 **When something looks wrong, check modifier order.** Swapping `.padding()` and `.background()` changes the result entirely.

13.6 **When a fixit suggestion appears, read it before accepting.** Fixits are often correct but sometimes mask a deeper issue. A fixit that says "add @Sendable" might be covering up an architecture problem.

_13.7 **"If body runs fresh every time, where does my data go?"** `body` only describes what the screen looks like — it's the drawing, not the data. Your actual data lives somewhere else. `@State` holds it in memory while the app is running. SwiftData saves it to disk so it survives after the app closes. CloudKit syncs it across devices. Think of it like a whiteboard (the screen) and a filing cabinet (persistence <<Glossary: Persistence>>). You can erase and redraw the whiteboard as often as you want without losing what's in the cabinet. *(See also: Chapter 15 for SwiftData and Core Data.)*

---

*Claude's Xcode 26 Swift Bible — Chapter 2*
*By Dr. Wahl — co-authored by Claude A. and Michael Fluharty. Swift 6, Xcode 26.*
