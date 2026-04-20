# Chapter 08: Lists, Grids, and ForEach

## List

The workhorse of data display in SwiftUI. Provides scrolling, cell recycling, selection, swipe actions, and platform-native styling for free.

### Basic List

```swift
struct ItemListView: View {
    let items: [Item]

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
    }
}
```

This requires `Item` to conform to `Identifiable`. If it does not, provide a key path:

```swift
List(names, id: \.self) { name in
    Text(name)
}
```

### Static Content

```swift
List {
    Text("First")
    Text("Second")
    Text("Third")
}
```

### Mixed Static and Dynamic

```swift
List {
    Section("Favorites") {
        ForEach(favorites) { item in
            Text(item.name)
        }
    }

    Section("All Items") {
        ForEach(allItems) { item in
            Text(item.name)
        }
    }
}
```

---

## ForEach

`ForEach` is not a loop — it is a view that generates views from a collection.

### With Identifiable Data

```swift
ForEach(recipes) { recipe in
    RecipeRow(recipe: recipe)
}
```

### With id Key Path

```swift
ForEach(names, id: \.self) { name in
    Text(name)
}
```

### With Index

```swift
ForEach(Array(items.enumerated()), id: \.element.id) { index, item in
    Text("\(index + 1). \(item.name)")
}
```

### Range-Based

```swift
ForEach(0..<5) { index in
    Text("Row \(index)")
}
```

### Watch Out

- `ForEach` with a range (`0..<count`) requires the range to be constant. If `count` changes, use `ForEach(0..<count, id: \.self)` — but better yet, use a real data collection.
- The `id` parameter is critical for performance. SwiftUI uses it to track which rows changed. If two items share the same ID, you get undefined behavior — wrong rows update, animations break.

---

## Identifiable Protocol

```swift
struct Recipe: Identifiable {
    let id = UUID()
    var name: String
    var cuisine: String
}
```

`Identifiable` requires a single property: `id`. It can be any `Hashable` type — `UUID`, `Int`, `String`.

### Watch Out

- `let id = UUID()` generates a new ID every time the struct is created. If you recreate structs from network data, use a stable identifier from the server instead.

---

## Sections

```swift
List {
    Section("Breakfast") {
        ForEach(breakfastItems) { item in
            Text(item.name)
        }
    }

    Section {
        ForEach(lunchItems) { item in
            Text(item.name)
        }
    } header: {
        Text("Lunch")
    } footer: {
        Text("All items under 500 calories")
    }
}
```

### Collapsible Sections (iOS 17+)

```swift
Section("Advanced", isExpanded: $isAdvancedExpanded) {
    Toggle("Debug Mode", isOn: $debugMode)
    Toggle("Verbose Logging", isOn: $verboseLogging)
}
```

---

## Swipe Actions

```swift
List {
    ForEach(messages) { message in
        MessageRow(message: message)
            .swipeActions(edge: .trailing) {
                Button(role: .destructive) {
                    delete(message)
                } label: {
                    Label("Delete", systemImage: "trash")
                }

                Button {
                    archive(message)
                } label: {
                    Label("Archive", systemImage: "archivebox")
                }
                .tint(.blue)
            }
            .swipeActions(edge: .leading) {
                Button {
                    toggleRead(message)
                } label: {
                    Label("Read", systemImage: "envelope.open")
                }
                .tint(.green)
            }
    }
}
```

### Watch Out

- The first trailing swipe action with `role: .destructive` gets a full-swipe gesture for quick deletion. Be careful — users may trigger it accidentally.
- Swipe actions only work inside a `List`. They do nothing in a `ScrollView` or `LazyVStack`.

---

## onDelete and onMove

The classic List editing modifiers. These work on `ForEach`, not on `List` directly.

```swift
List {
    ForEach(items) { item in
        Text(item.name)
    }
    .onDelete(perform: deleteItems)
    .onMove(perform: moveItems)
}
.toolbar {
    EditButton()
}

func deleteItems(at offsets: IndexSet) {
    items.remove(atOffsets: offsets)
}

func moveItems(from source: IndexSet, to destination: Int) {
    items.move(fromOffsets: source, toOffset: destination)
}
```

### Watch Out

- `onDelete` adds the standard swipe-to-delete gesture. If you also use `.swipeActions`, `onDelete` is ignored — `.swipeActions` takes priority.
- `onMove` only works when the List is in edit mode. Add an `EditButton()` to the toolbar.

---

## Refreshable

Pull-to-refresh. The closure is `async`, so you can `await` network calls directly.

```swift
List(items) { item in
    Text(item.name)
}
.refreshable {
    await loadItems()
}
```

### Watch Out

- `.refreshable` only works on scrollable views (`List`, `ScrollView`). It does nothing on a plain `VStack`.
- The refresh indicator stays visible until the `async` closure completes. If your network call is fast, the spinner may flash briefly. That is expected.

---

## Searchable

Adds a search bar to a `NavigationStack` or `NavigationSplitView`.

```swift
struct RecipeListView: View {
    @State private var searchText = ""
    let recipes: [Recipe]

    var filteredRecipes: [Recipe] {
        if searchText.isEmpty {
            return recipes
        }
        return recipes.filter { $0.name.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filteredRecipes) { recipe in
                Text(recipe.name)
            }
            .navigationTitle("Recipes")
            .searchable(text: $searchText, prompt: "Find a recipe")
        }
    }
}
```

### Search Suggestions

```swift
.searchable(text: $searchText) {
    ForEach(suggestions, id: \.self) { suggestion in
        Text(suggestion).searchCompletion(suggestion)
    }
}
```

### Search Scopes

```swift
.searchable(text: $searchText)
.searchScopes($searchScope) {
    Text("All").tag(SearchScope.all)
    Text("Name").tag(SearchScope.name)
    Text("Ingredient").tag(SearchScope.ingredient)
}
```

### Watch Out

- `.searchable` must be inside a `NavigationStack` or `NavigationSplitView`. Outside of navigation, the search bar does not appear.
- The search bar placement varies by platform. On iOS it is under the navigation title; on macOS it is in the toolbar.

---

## List Styles

```swift
List { ... }
    .listStyle(.plain)          // no grouped background
    .listStyle(.inset)          // padded from edges
    .listStyle(.grouped)        // iOS grouped sections
    .listStyle(.insetGrouped)   // rounded grouped sections (iOS default in many contexts)
    .listStyle(.sidebar)        // macOS sidebar style, disclosure triangles
```

### Row Customization

```swift
List {
    ForEach(items) { item in
        Text(item.name)
            .listRowBackground(Color.yellow.opacity(0.2))
            .listRowSeparator(.hidden)
            .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
    }
}
```

---

## Selection

### Single Selection

```swift
@State private var selected: Item.ID?

List(items, selection: $selected) { item in
    Text(item.name)
}
```

### Multiple Selection

```swift
@State private var selected: Set<Item.ID> = []

List(items, selection: $selected) { item in
    Text(item.name)
}
.toolbar { EditButton() }
```

Multiple selection requires edit mode on iOS. On macOS, it works directly with Command-click and Shift-click.

---

## LazyVGrid and LazyHGrid

For grid layouts. These live inside a `ScrollView`, not a `List`.

### LazyVGrid (Vertical Scrolling Grid)

```swift
let columns = [
    GridItem(.adaptive(minimum: 150))
]

ScrollView {
    LazyVGrid(columns: columns, spacing: 16) {
        ForEach(photos) { photo in
            PhotoCard(photo: photo)
        }
    }
    .padding()
}
```

### LazyHGrid (Horizontal Scrolling Grid)

```swift
let rows = [
    GridItem(.fixed(100)),
    GridItem(.fixed(100))
]

ScrollView(.horizontal) {
    LazyHGrid(rows: rows, spacing: 12) {
        ForEach(items) { item in
            ItemCard(item: item)
        }
    }
    .padding()
}
```

---

## GridItem

`GridItem` defines how columns (in `LazyVGrid`) or rows (in `LazyHGrid`) are sized.

### .fixed

Exact size. The column is always this wide.

```swift
GridItem(.fixed(120))
```

### .flexible

Grows to fill available space, within optional min/max bounds.

```swift
GridItem(.flexible())                           // fills available space
GridItem(.flexible(minimum: 100, maximum: 200)) // bounded
```

### .adaptive

Fits as many columns as possible within the available width. This is the most useful for responsive grids.

```swift
GridItem(.adaptive(minimum: 150))
// On a 390pt iPhone: 2 columns
// On a 1024pt iPad: 6 columns
// Adjusts automatically when the device rotates
```

### Combining Grid Items

```swift
let columns = [
    GridItem(.fixed(60)),           // narrow first column
    GridItem(.flexible()),          // fills remaining space
    GridItem(.flexible())           // shares remaining space
]
```

### Watch Out

- `.adaptive` creates as many columns as fit. You do not control the exact count — it is calculated from available width and the minimum size. If you want exactly 3 columns, use three `.flexible()` items.
- Grid items accept `spacing` and `alignment` parameters: `GridItem(.flexible(), spacing: 8, alignment: .top)`.

---

## ScrollView

### Basic Scroll View

```swift
ScrollView {
    VStack(spacing: 12) {
        ForEach(items) { item in
            ItemCard(item: item)
        }
    }
    .padding()
}
```

### Horizontal Scroll

```swift
ScrollView(.horizontal, showsIndicators: false) {
    HStack(spacing: 16) {
        ForEach(featured) { item in
            FeaturedCard(item: item)
                .frame(width: 280)
        }
    }
    .padding(.horizontal)
}
```

### Scroll Position (iOS 17+)

```swift
@State private var scrollPosition: Item.ID?

ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
    .scrollTargetLayout()
}
.scrollPosition(id: $scrollPosition)
```

Programmatically scroll by setting `scrollPosition` to an item's ID.

### Watch Out

- `ScrollView` does not recycle views. Every view in a `ScrollView` is created immediately unless you use `LazyVStack` or `LazyHStack` inside it.
- `.scrollIndicators(.hidden)` hides the scrollbar. Use it for horizontal carousels. Avoid hiding it for vertical content — users need the scrollbar to orient themselves.

---

## LazyVStack and LazyHStack

These create views on demand as they scroll into view. Essential for large data sets.

```swift
ScrollView {
    LazyVStack(spacing: 12) {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}
```

### Pinned Headers

```swift
ScrollView {
    LazyVStack(spacing: 12, pinnedViews: [.sectionHeaders]) {
        ForEach(sections) { section in
            Section {
                ForEach(section.items) { item in
                    ItemRow(item: item)
                }
            } header: {
                Text(section.title)
                    .font(.headline)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(.bar)
            }
        }
    }
}
```

### Performance: Lazy vs Eager

| Container | View Creation | Use When |
|-----------|--------------|----------|
| `VStack` | All at once | Small collections (under 50 items) |
| `LazyVStack` | On demand | Large or unbounded collections |
| `List` | On demand (with recycling) | Data lists needing swipe actions, selection |
| `LazyVGrid` | On demand | Grid layouts in ScrollView |

### Watch Out

- `LazyVStack` creates views as they scroll in, but does not destroy them when they scroll out. For very long lists (thousands of items), memory grows over time. `List` handles this better because it recycles cells.
- Do not put a `LazyVStack` inside a `List`. The List already handles lazy loading. Nesting them causes layout conflicts.
- `LazyVStack` does not support swipe actions, onDelete, or onMove. Those are `List`-only features.
- `LazyVStack` alignment defaults to `.center`. For left-aligned content, use `LazyVStack(alignment: .leading)`.

---

## Practical Tips

1. **Use `List` by default** for data that needs selection, swipe actions, or editing. Switch to `ScrollView` + `LazyVStack` when you need custom layouts or grid arrangements.

2. **Always provide stable IDs.** Using array indices as IDs causes incorrect animations and state bugs when items are inserted or removed.

3. **`.adaptive` GridItem is your friend** for responsive layouts that work across iPhone, iPad, and Mac without conditional logic.

4. **Combine `.searchable` and `.refreshable`** on the same List for a standard data browsing experience with minimal code.

5. **Test with large data sets.** A list that works fine with 10 items may stutter at 10,000. Profile with Instruments if scrolling feels slow.

6. **Prefer `LazyVStack` over `VStack`** inside a `ScrollView` any time the content count is dynamic or could grow. The memory difference is significant.

7. **Section headers and footers** in List get automatic styling. In `LazyVStack` with `pinnedViews`, you style them yourself — but you get sticky headers for free.
