# Chapter 20: Performance, Instruments, & Best Practices

**Claude's Swift Reference 26** -- Part V: Advanced Techniques

---

## What You'll Learn

By the end of this chapter you can:

- Launch Instruments from Xcode and read the three templates you'll actually use most: Time Profiler, Allocations, and SwiftUI.
- Spot and stop unnecessary SwiftUI `body` recomputations.
- Avoid the two most common `@StateObject` / `@ObservedObject` mistakes.
- Keep actors from becoming bottlenecks in Swift 6 concurrency.
- Apply a small set of habits that make an app stay smooth as it grows.

---

## When to Start Profiling

Don't profile before there's a problem. The old saying "premature optimization is the root of all evil" applies: guessing what's slow is usually wrong, and guessing-based changes make code harder to read without making it faster.

Start profiling when you see one of these:

- The UI stutters while scrolling, typing, or animating.
- The Xcode Debug Navigator shows CPU or memory climbing past what feels reasonable.
- A specific action (save, open, search) feels laggy.

Profile with real user scenarios on a real device, not the simulator. The simulator gives you roughly the host Mac's speed, which hides problems that bite on an actual iPhone.

---

## Launching Instruments

From Xcode: **Product > Profile** (`⌘I`) with a physical device attached. Instruments opens the template picker. The three templates you use 95% of the time:

- **Time Profiler** -- where is the app spending CPU?
- **Allocations** -- what objects are being created, how many, and how long do they live?
- **SwiftUI** -- which views are re-rendering, and how often?

Start with Time Profiler when the symptom is "slow or stuttering." Start with SwiftUI when the symptom is "the screen flickers or my animations jump." Start with Allocations when memory is climbing.

---

## Time Profiler

Click Record, use the app the way the slow case uses it, click Stop. You get a flame-graph-style view: tall columns are where the CPU spent the most time.

### Reading the Trace

- **Call tree** in the bottom pane. Expand it by heaviest-first (right-click > "Invert Call Tree" if you want the hottest leaves at the top).
- **Bold entries** are your app's code. Grayed-out entries are Apple frameworks.
- **Percentage column** tells you what fraction of wall-clock time was spent in that function.

Look for code you wrote consuming a surprising percentage. If `ContentView.body` is eating 40% of CPU during a scroll, that's your fix.

### Flame-Graph View

Switch the display to Flamegraph for a scrollable, visual summary. Wider bars = more time. Click a bar to jump to the source file.

---

## SwiftUI Instrument

The SwiftUI template records every view-body call. Two columns matter:

- **Call count** -- how many times each view's `body` ran.
- **Duration** -- total time spent in that body.

If a single `Text` row's `body` is being called thousands of times during a short interaction, something above it is re-rendering unnecessarily. That's almost always a fix in the parent: an observable-object update that's too coarse-grained, or a state change that shouldn't be triggering a repaint.

---

## Common SwiftUI Performance Mistakes

### `@StateObject` vs. `@ObservedObject`

**Rule:** if the view creates the object, use `@StateObject`. If the object is handed in from outside, use `@ObservedObject`.

Wrong (object recreates on every parent re-render):
```swift
struct BadParent: View {
    var body: some View {
        Child()
    }
}

struct Child: View {
    @ObservedObject var model = Model()   // ← recreated every render
    var body: some View { Text(model.title) }
}
```

Right:
```swift
struct Child: View {
    @StateObject private var model = Model()   // ← created once, persists
    var body: some View { Text(model.title) }
}
```

The `@Observable` macro (Swift 5.9+) avoids this trap entirely:
```swift
@Observable
final class Model { var title = "" }

struct Child: View {
    @State private var model = Model()
    var body: some View { Text(model.title) }
}
```

### Passing Too Much Into a View

The more properties a view takes, the more reasons it has to re-render. If `ProfileCard(user: user)` takes the whole user but only renders the name, SwiftUI re-renders when any user property changes. Pass only what you need:

```swift
ProfileCard(name: user.name)
```

Or split the model into smaller `@Observable` classes so only the relevant piece triggers updates.

### Lists That Aren't Stable

`List` and `ForEach` rely on stable `id` values to animate inserts, deletes, and updates without re-rendering the whole list. Give every row a real identity:

```swift
ForEach(items, id: \.id) { item in Row(item: item) }
```

Using `id: \.self` on mutable value types, or generating a fresh `UUID` on every render, defeats the identity check and forces a full redraw.

### `AsyncImage` Without Caching

`AsyncImage` does no caching. If the user scrolls past an image, then back, it re-downloads. For serious image use, reach for a caching library (Kingfisher, Nuke) or cache manually in a model.

---

## Actor Contention

Swift 6's concurrency makes actors safe. It can also make them slow if a single actor is a choke point.

### The Problem

```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    func image(for url: URL) async -> UIImage { /* load and store */ }
}
```

If every view on screen asks the cache for its image, they all serialize through this one actor. The first one gets serviced fast, the rest queue up.

### The Fixes

1. **Narrow the `await`.** If the work you do on the actor is just "look up in a dictionary," let the actor return the cached value fast, but perform the expensive load off-actor.

2. **Split the actor.** Two actors can't compete with each other, and each serves a different slice of the work.

3. **Use `nonisolated` methods for reads that don't touch mutable state.** Those don't go through the actor's execution queue.

4. **Use `.task` with IDs to cancel in-flight work.** When a row scrolls offscreen, cancel the image load rather than letting it finish.

---

## Everyday Habits

The cheapest performance wins aren't about profiling; they're habits that keep an app fast by default.

- **Keep view hierarchies shallow.** Deep nesting makes SwiftUI's diffing more expensive and makes the code harder to read.
- **Pull state up only as far as it needs to go.** State owned by a grandparent triggers more re-renders than state owned by the immediate parent.
- **Avoid expensive computations in `body`.** Compute once in a helper method (or outside the view) and pass the result in.
- **Prefer `@Observable` over `ObservableObject`.** Finer-grained tracking means fewer spurious re-renders.
- **Measure before and after.** If you "optimized" something, run Instruments again to confirm. Most optimizations don't help; some make things worse.

---

## Chapter Mini-Example -- A Fast List With 10,000 Items

A `List` that renders 10,000 rows smoothly, because it does the right things by default:

```swift
import SwiftUI

struct Row: Identifiable {
    let id: Int
    let title: String
    let subtitle: String
}

struct BigList: View {
    let rows: [Row] = (0..<10_000).map {
        Row(id: $0, title: "Item \($0)", subtitle: "Subtitle \($0)")
    }

    var body: some View {
        List(rows) { row in
            HStack {
                Text(row.title).font(.headline)
                Spacer()
                Text(row.subtitle).foregroundStyle(.secondary)
            }
        }
    }
}
```

Why this is fast:

- `Row` has a stable `id: Int`. `List` can diff efficiently on inserts / deletes.
- The row view has no `@ObservedObject` or heavy computation.
- We don't wrap the list in a `GeometryReader` or force it into a custom layout.
- The strings are computed up front, not rebuilt in `body`.

Run Instruments (Time Profiler) on this; scrolling should spend near-zero CPU. That's the shape you're aiming for when your own lists feel slow.

---

## What Book 21 Does

Part V closes with performance. Part VI is the toolchain beyond the code itself. Book 21 covers Git and GitHub -- how to version your work, share it with a remote, and participate in the standard open-source workflow.
