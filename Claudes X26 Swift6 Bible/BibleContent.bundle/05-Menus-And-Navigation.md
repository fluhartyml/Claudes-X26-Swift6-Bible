# Chapter 05: Menus and Navigation

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
