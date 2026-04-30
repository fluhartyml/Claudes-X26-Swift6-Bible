# Chapter 05: Menus and Navigation

## Live Reference: Inkwell sidebar + LockBox three-column + CryoTunes tabs

> Three different production navigation shapes ship across the book's app roster. **Inkwell** uses a sidebar-and-detail `NavigationSplitView` for the book's Parts → Books → Chapters → Pages tree (the navigation you're using right now to get to this page). **Claudes LockBox** uses a three-column `NavigationSplitView` (Folders → Items → Detail) plus a TabView at the root level (Vault tab + Under the Hood tab). **CryoTunes Player** uses a flat tab-and-control-cluster pattern fitted to a music player's needs. Reading the three side-by-side shows how the same `NavigationStack` / `NavigationSplitView` / `TabView` primitives compose into very different feeling apps. Sources: [Inkwell](https://github.com/fluhartyml/Claudes-X26-Swift6-Bible), [LockBox](https://github.com/fluhartyml/Claudes-LockBox), [CryoTunes Player](https://github.com/fluhartyml/CryoTunesPlayer). See Build-Along 00, Build-Along 03, Source Tour 18.

---

## X26 Menu and Toolbar Updates

Menus have a refreshed look across platforms in X26. They adopt the Liquid Glass material, and menu items for common actions surface system icons to help users scan and identify them quickly[^mn1]. New to iPadOS in X26: apps now have a **menu bar** for faster access to common commands, similar in spirit to a Mac menu bar.

### Adopt Standard Selectors for Menu Item Icons

For menu items that perform standard actions like Cut, Copy, and Paste, the system uses the menu item's selector to determine which icon to apply. To pick up icons in those menu items with no extra code, use the standard selectors. Custom action selectors don't get system icons; you have to provide them yourself.

A practical follow-on rule: match the actions you surface at the top of a contextual menu to the swipe actions you provide for the same item. Consistency between contextual menu and swipe surfaces is what keeps both predictable.

### Toolbar Grouping with `ToolbarSpacer`

Toolbars adopt Liquid Glass and gain a real grouping mechanism. You decide which actions belong together by separating groups with a fixed spacer:

```swift
.toolbar {
    ToolbarItemGroup(placement: .primaryAction) {
        Button("Undo") { undo() }
        Button("Redo") { redo() }
    }
    ToolbarSpacer(.fixed)
    ToolbarItemGroup(placement: .primaryAction) {
        Button("Markup") { markup() }
        Menu("More") { /* ... */ }
    }
}
```

Items within the same group share a Liquid Glass background. Items separated by `ToolbarSpacer(.fixed)` get their own background. The pattern Apple flags as wrong is putting four unrelated buttons together with one shared background; the right pattern is grouping by function (undo/redo together, markup/more together) and letting the spacer divide them visually.

UIKit and AppKit have parallel APIs (`fixed` spacer in UIKit, `ToolbarSpacer` in AppKit).

### Use Icons for Common Actions; Always Provide Accessibility Labels

Apple's guidance: prefer icons over text for common toolbar actions to declutter the interface. For consistency, don't mix text and icons across items that share a background — pick one style per group. And regardless of what you show in the UI, **always provide an accessibility label** for every icon. Users who turn on VoiceOver or Voice Control opt into the text label that way; the icon-only visual stays clean for everyone else.

### Hide Toolbar Items Properly

If you've ever seen an empty toolbar slot in a shipping app, that's usually the developer hiding the *content* of a toolbar item rather than the item itself. The fix is to hide the entire toolbar item with `.hidden(_:)` on the item, not on its content. The empty slot disappears completely.

[^mn1]: Apple Developer Documentation, *Adopting Liquid Glass*. <https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass> — verified 2026-04-29.

---

## NavigationStack

The modern replacement for `NavigationView`. Use this for single-column, push-pop navigation on iPhone and iPad.

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Settings", value: "settings")
                NavigationLink("Profile", value: "profile")
            }
            .navigationTitle("Home")
            .navigationDestination(for: String.self) { value in
                DetailView(item: value)
            }
        }
    }
}
```

### Programmatic Navigation with Path

Use `NavigationPath` when you need to push/pop views from code — after a network call, a button tap, or a deep link.

```swift
struct AppView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Button("Go to Step 1") {
                    path.append("step1")
                }
                Button("Jump to Step 3") {
                    path.append("step1")
                    path.append("step2")
                    path.append("step3")
                }
            }
            .navigationTitle("Start")
            .navigationDestination(for: String.self) { step in
                StepView(step: step, path: $path)
            }
        }
    }
}

struct StepView: View {
    let step: String
    @Binding var path: NavigationPath

    var body: some View {
        VStack {
            Text("Current: \(step)")
            Button("Back to Root") {
                path = NavigationPath() // clears entire stack
            }
        }
        .navigationTitle(step)
    }
}
```

### Typed Navigation Path

When all your destinations share a single type, skip `NavigationPath` and use a plain array.

```swift
struct RecipeApp: View {
    @State private var path: [Recipe] = []

    var body: some View {
        NavigationStack(path: $path) {
            RecipeListView()
                .navigationDestination(for: Recipe.self) { recipe in
                    RecipeDetailView(recipe: recipe)
                }
        }
    }
}
```

### Watch Out

- `NavigationPath` is type-erased. It can hold any `Hashable` type, but you need a `.navigationDestination(for:)` registered for each type you append.
- If you append a value with no matching destination, the push silently fails. No crash, no error. Just nothing happens.
- Do not nest `NavigationStack` inside another `NavigationStack`. You get double navigation bars and broken behavior.

---

## NavigationSplitView

For two- or three-column layouts. iPad and Mac get real columns; iPhone collapses to a stack automatically.

### Two-Column

```swift
struct TwoColumnView: View {
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            List(items, selection: $selectedItem) { item in
                Text(item.name)
            }
            .navigationTitle("Items")
        } detail: {
            if let selectedItem {
                ItemDetailView(item: selectedItem)
            } else {
                ContentUnavailableView("Select an Item",
                    systemImage: "tray",
                    description: Text("Pick something from the sidebar."))
            }
        }
    }
}
```

### Three-Column

```swift
NavigationSplitView {
    // Sidebar (column 1)
    CategoryListView(selection: $selectedCategory)
} content: {
    // Content (column 2)
    if let selectedCategory {
        ItemListView(category: selectedCategory, selection: $selectedItem)
    }
} detail: {
    // Detail (column 3)
    if let selectedItem {
        ItemDetailView(item: selectedItem)
    }
}
```

### Controlling Column Visibility

```swift
@State private var columnVisibility: NavigationSplitViewVisibility = .all

NavigationSplitView(columnVisibility: $columnVisibility) {
    Sidebar()
} detail: {
    Detail()
}
```

Options: `.all`, `.doubleColumn`, `.detailOnly`, `.automatic`.

### Watch Out

- On iPhone, `NavigationSplitView` collapses into a single navigation stack. The sidebar becomes the root list. This is automatic but test it — your layout assumptions may not hold.
- `selection` binding on `List` inside `NavigationSplitView` drives navigation. If you also use `NavigationLink(value:)`, you can get conflicts. Pick one approach.

---

## NavigationLink

Two forms exist: the modern value-based form and the older view-based form.

### Value-Based (Preferred)

```swift
NavigationLink("Show Detail", value: myItem)
```

Pair with `.navigationDestination(for:)` on a parent. The destination is declared once, not per link.

### View-Based (Legacy but Functional)

```swift
NavigationLink("Show Detail") {
    DetailView(item: myItem)
}
```

This still works. The downside is that the destination view is created at the same time as the link, even if the user never taps it. For heavy views, that wastes memory.

### Custom Label

```swift
NavigationLink(value: recipe) {
    HStack {
        Image(systemName: "fork.knife")
        VStack(alignment: .leading) {
            Text(recipe.name).font(.headline)
            Text(recipe.cuisine).font(.caption).foregroundStyle(.secondary)
        }
    }
}
```

---

## Navigation Title

```swift
.navigationTitle("Recipes")             // standard
.navigationTitle($editableTitle)         // editable title (iOS 16+)
```

### Display Modes (iOS)

```swift
.navigationBarTitleDisplayMode(.large)     // big title, scrolls to inline
.navigationBarTitleDisplayMode(.inline)    // small centered title
.navigationBarTitleDisplayMode(.automatic) // inherits from parent
```

### Watch Out

- `.navigationTitle` goes on the content inside the NavigationStack, not on the NavigationStack itself. Put it on the `List` or `VStack`, not the outer container.

---

## TabView

### Basic Tabs

```swift
struct MainView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            Tab("Home", systemImage: "house", value: 0) {
                HomeView()
            }
            Tab("Search", systemImage: "magnifyingglass", value: 1) {
                SearchView()
            }
            Tab("Settings", systemImage: "gear", value: 2) {
                SettingsView()
            }
        }
    }
}
```

### Badge

```swift
Tab("Inbox", systemImage: "tray", value: 0) {
    InboxView()
}
.badge(unreadCount)
```

### Watch Out

- Each tab should contain its own `NavigationStack` if it needs navigation. Do not wrap the entire `TabView` in a `NavigationStack`.
- Tab state resets when switching tabs unless you preserve it with `@State` or `@SceneStorage`.

---

## macOS Menu Bar

### CommandGroup: Adding to Existing Menus

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandGroup(replacing: .newItem) {
                Button("New Recipe") {
                    // action
                }
                .keyboardShortcut("n", modifiers: .command)
            }

            CommandGroup(after: .sidebar) {
                Button("Toggle Inspector") {
                    // action
                }
                .keyboardShortcut("i", modifiers: [.command, .option])
            }
        }
    }
}
```

Common placements: `.newItem`, `.saveItem`, `.sidebar`, `.toolbar`, `.help`, `.pasteboard`, `.undoRedo`.

### CommandMenu: Custom Top-Level Menu

```swift
.commands {
    CommandMenu("Recipes") {
        Button("Import from File...") { importRecipes() }
            .keyboardShortcut("i", modifiers: [.command, .shift])

        Divider()

        Button("Export All...") { exportRecipes() }

        Menu("Sort By") {
            Button("Name") { sortBy(.name) }
            Button("Date Added") { sortBy(.date) }
            Button("Rating") { sortBy(.rating) }
        }
    }
}
```

### Watch Out

- Menu commands cannot directly access view state. Use `@FocusedValue` or `@FocusedBinding` to bridge between the menu bar and the focused view.
- `.commands` modifier goes on the `Scene`, not on a `View`.

### FocusedValue Bridge

```swift
// 1. Define the key
struct FocusedRecipeKey: FocusedValueKey {
    typealias Value = Binding<Recipe>
}

extension FocusedValues {
    var selectedRecipe: Binding<Recipe>? {
        get { self[FocusedRecipeKey.self] }
        set { self[FocusedRecipeKey.self] = newValue }
    }
}

// 2. Publish from the view
struct RecipeDetailView: View {
    @Binding var recipe: Recipe

    var body: some View {
        Text(recipe.name)
            .focusedSceneValue(\.selectedRecipe, $recipe)
    }
}

// 3. Consume in the menu command
struct MyApp: App {
    @FocusedBinding(\.selectedRecipe) var focusedRecipe

    var body: some Scene {
        WindowGroup { ContentView() }
        .commands {
            CommandMenu("Recipe") {
                Button("Mark as Favorite") {
                    focusedRecipe?.isFavorite = true
                }
                .disabled(focusedRecipe == nil)
            }
        }
    }
}
```

---

## Context Menus

```swift
Text("Hold me")
    .contextMenu {
        Button("Copy", action: copyItem)
        Button("Delete", role: .destructive, action: deleteItem)

        Divider()

        Menu("Share") {
            Button("Messages", action: shareViaMessages)
            Button("Mail", action: shareViaMail)
        }
    }
```

### Context Menu with Preview

```swift
Text(recipe.name)
    .contextMenu {
        Button("Edit") { editRecipe() }
        Button("Delete", role: .destructive) { deleteRecipe() }
    } preview: {
        RecipePreviewCard(recipe: recipe)
            .frame(width: 300, height: 200)
    }
```

### Watch Out

- Context menus only support `Button`, `Divider`, `Menu`, `Toggle`, and `Picker`. No arbitrary views — no sliders, no text fields.
- On macOS, context menus trigger on right-click. On iOS, long press.

---

## Practical Tips

1. **Start with NavigationStack.** Only move to NavigationSplitView when you actually need columns (iPad/Mac sidebar layouts).

2. **Use value-based NavigationLink** with `.navigationDestination(for:)`. It separates the "what to show" from the "where it lives" and enables programmatic navigation.

3. **Pop to root** by resetting the path: `path = NavigationPath()` or `path.removeLast(path.count)`.

4. **Deep linking**: Build your `NavigationPath` from URL components on app launch, then set it as the initial path.

5. **Test on all platforms.** NavigationSplitView behaves very differently on iPhone vs iPad vs Mac. The compiler will not catch layout surprises.

6. **Keep NavigationStack out of reusable components.** The view that owns the NavigationStack should be a top-level coordinator, not a leaf view.
