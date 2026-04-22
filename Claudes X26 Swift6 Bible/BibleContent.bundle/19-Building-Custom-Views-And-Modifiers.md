# Chapter 19: Building Custom Views & Modifiers

**Claude's Swift Reference 26** -- Part V: Advanced Techniques

---

## What You'll Learn

By the end of this chapter you can:

- Extract reusable SwiftUI views from copy-pasted snippets.
- Write custom `ViewModifier` types and apply them with `.modifier` or a cleaner `.myStyle()` extension.
- Use `@Environment` values to pass data deep into a view tree without threading it through every level.
- Read child-view sizes and positions with `GeometryReader`.
- Share data from child to parent with `PreferenceKey`.
- Animate transitions between layouts with `.matchedGeometryEffect`.

---

## Extracting a Custom View

The first step past "all code in one big `ContentView`" is pulling repeated shapes into their own `View` types.

```swift
struct AvatarRow: View {
    let name: String
    let imageName: String

    var body: some View {
        HStack {
            Image(systemName: imageName)
                .resizable()
                .scaledToFit()
                .frame(width: 40, height: 40)
                .foregroundStyle(.blue)
            Text(name).font(.headline)
            Spacer()
        }
        .padding()
    }
}
```

Used anywhere:

```swift
VStack {
    AvatarRow(name: "Ada",    imageName: "person.circle")
    AvatarRow(name: "Max",    imageName: "person.circle.fill")
    AvatarRow(name: "Claude", imageName: "sparkles")
}
```

**The rule of three**: the third time you write the same layout, turn it into a view.

---

## ViewModifier -- Reusable Styling

When the thing you keep repeating is a **stack of modifiers**, not a layout, reach for `ViewModifier` instead of a new view.

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
            .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
    }
}
```

Apply it with `.modifier(CardStyle())`, or -- for a cleaner call site -- add a `View` extension:

```swift
extension View {
    func card() -> some View { modifier(CardStyle()) }
}

// Usage
Text("Hello")
    .card()
```

Custom modifiers are how you ship a house style. A dozen views across the app, one definition, any future tweak happens in one place.

### Modifiers That Take Arguments

```swift
struct BadgedStyle: ViewModifier {
    let color: Color
    let count: Int

    func body(content: Content) -> some View {
        content.overlay(alignment: .topTrailing) {
            if count > 0 {
                Text("\(count)")
                    .font(.caption2.bold())
                    .padding(4)
                    .background(color, in: Circle())
                    .foregroundStyle(.white)
                    .offset(x: 8, y: -8)
            }
        }
    }
}

extension View {
    func badged(_ count: Int, color: Color = .red) -> some View {
        modifier(BadgedStyle(color: color, count: count))
    }
}

// Usage
Image(systemName: "envelope")
    .font(.title)
    .badged(3)
```

---

## Environment Values -- Passing State Without Plumbing

When deeply nested views need the same value (theme, date formatter, API client), don't thread it through every initializer. Put it in the environment.

### Reading a Built-In Environment Value

```swift
struct Banner: View {
    @Environment(\.colorScheme) private var scheme

    var body: some View {
        Text("Hello")
            .foregroundStyle(scheme == .dark ? .white : .black)
    }
}
```

### Defining Your Own Environment Value

Define a key, extend `EnvironmentValues`, and set it with `.environment`:

```swift
private struct ThemeKey: EnvironmentKey {
    static let defaultValue: Color = .blue
}

extension EnvironmentValues {
    var theme: Color {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// A view that reads it
struct ThemedButton: View {
    @Environment(\.theme) private var theme
    let title: String

    var body: some View {
        Text(title).padding().background(theme).foregroundStyle(.white)
    }
}

// A view tree that sets it
VStack {
    ThemedButton(title: "Save")
    ThemedButton(title: "Cancel")
}
.environment(\.theme, .orange)
```

Every `ThemedButton` under that `.environment(...)` sees orange. Change the value once and every button updates.

---

## GeometryReader -- Reading the Size Around You

`GeometryReader` gives its child view a `GeometryProxy` describing the size and safe-area it has been allocated.

```swift
struct SplitHalf: View {
    var body: some View {
        GeometryReader { geo in
            HStack(spacing: 0) {
                Color.red.frame(width: geo.size.width / 2)
                Color.blue.frame(width: geo.size.width / 2)
            }
        }
    }
}
```

### When Not to Use GeometryReader

`GeometryReader` expands to fill the space it is offered, which often surprises newcomers. If all you need is "half the width," reach for `.frame(maxWidth: .infinity)` and let SwiftUI's normal layout system do the work.

Use `GeometryReader` when you genuinely need to compute something from the runtime size -- a custom layout, a parallax effect, a shape that depends on width / height.

### `onGeometryChange` (iOS 18+)

In iOS 18, `.onGeometryChange` observes a view's frame without wrapping it in `GeometryReader`:

```swift
Text("Hello")
    .onGeometryChange(for: CGSize.self) { proxy in
        proxy.size
    } action: { newSize in
        print("I am now", newSize)
    }
```

Cleaner than `GeometryReader` when you only need a measurement, not a layout container.

---

## PreferenceKey -- Child to Parent Communication

The environment passes data **down** the view tree. Preference keys pass data **up**.

```swift
private struct HeightKey: PreferenceKey {
    static let defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct RowLikeContent: View {
    var body: some View {
        Text("I report my height upward")
            .background(
                GeometryReader { geo in
                    Color.clear.preference(key: HeightKey.self, value: geo.size.height)
                }
            )
    }
}

struct Parent: View {
    @State private var rowHeight: CGFloat = 0

    var body: some View {
        VStack {
            RowLikeContent()
            Text("The row above is \(Int(rowHeight)) points tall")
        }
        .onPreferenceChange(HeightKey.self) { rowHeight = $0 }
    }
}
```

`reduce` is how SwiftUI combines values from multiple children; in this case we take the largest. Use preference keys when a parent needs to size itself based on its children, or when a child needs to say something specific to an ancestor.

---

## matchedGeometryEffect -- Transitions Between Layouts

When the same "thing" appears in two different layouts, `matchedGeometryEffect` animates it between them.

```swift
struct PhotoDetail: View {
    @Namespace private var ns
    @State private var expanded = false

    var body: some View {
        VStack {
            if expanded {
                Image("kitten")
                    .resizable()
                    .scaledToFit()
                    .matchedGeometryEffect(id: "photo", in: ns)
                    .onTapGesture { withAnimation(.spring) { expanded.toggle() } }
            } else {
                HStack {
                    Image("kitten")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 80, height: 80)
                        .matchedGeometryEffect(id: "photo", in: ns)
                        .onTapGesture { withAnimation(.spring) { expanded.toggle() } }
                    Text("Kitten").font(.headline)
                }
            }
        }
    }
}
```

Tap the image. SwiftUI notices the two views share the `id: "photo"` in the same namespace, and animates position + size from the small version to the full one (and back). You don't write any of the intermediate frames.

`@Namespace` gives you a private namespace; reuse its value for every view pair you want matched.

---

## Chapter Mini-Example -- A Badge Stack

Putting custom views, a custom modifier, and an environment value together:

```swift
import SwiftUI

private struct AccentKey: EnvironmentKey { static let defaultValue: Color = .blue }
extension EnvironmentValues {
    var accent: Color {
        get { self[AccentKey.self] }
        set { self[AccentKey.self] = newValue }
    }
}

struct BadgedIcon: View {
    let systemName: String
    let count: Int

    @Environment(\.accent) private var accent

    var body: some View {
        Image(systemName: systemName)
            .font(.title)
            .foregroundStyle(accent)
            .overlay(alignment: .topTrailing) {
                if count > 0 {
                    Text("\(count)")
                        .font(.caption2.bold())
                        .padding(4)
                        .background(.red, in: Circle())
                        .foregroundStyle(.white)
                        .offset(x: 8, y: -8)
                }
            }
    }
}

struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content.padding()
            .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
            .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
    }
}

extension View { func card() -> some View { modifier(CardStyle()) } }

struct NotificationBar: View {
    var body: some View {
        HStack(spacing: 24) {
            BadgedIcon(systemName: "envelope", count: 3)
            BadgedIcon(systemName: "bell",     count: 0)
            BadgedIcon(systemName: "person.2", count: 1)
        }
        .card()
        .environment(\.accent, .orange)
    }
}
```

One reusable icon view, one reusable card modifier, one environment value -- and the bar's entire accent color lives in one spot.

---

## What Book 20 Does

We've added view-shaped tools to the toolkit. Book 20 pulls back and looks at the app as a running system: Instruments, profiling, and the habits that keep a SwiftUI app smooth as it grows.
