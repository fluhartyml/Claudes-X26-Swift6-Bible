# Chapter 15: SwiftData & CoreData

**Claude's Swift Reference 26** -- Part IV: The Application

---

## What You'll Learn

By the end of this chapter you can:

- Describe data models in Swift using SwiftData's `@Model` macro.
- Save, fetch, and delete model objects with a `ModelContainer` and a `ModelContext`.
- Drive a SwiftUI view from live SwiftData fetches with `@Query`.
- Decide when to reach for SwiftData vs. the older CoreData stack.
- Opt in to iCloud sync so the same data shows up on every device signed in to the user's Apple ID.

---

## The Short History

Every Apple app that stores structured data on-device uses one of three things:

1. **User Defaults** -- a tiny key-value store. Good for preferences, last-opened document, scroll position. Book 13's `@SceneStorage` and `@AppStorage` both wrap it.
2. **CoreData** -- the Objective-C-era object graph and persistence framework. Still supported, still powerful, still how SwiftData works under the hood.
3. **SwiftData** -- the Swift-native layer Apple introduced in 2023. Built on CoreData, exposed through Swift macros and property wrappers. What you should reach for first in new projects.

This chapter teaches SwiftData. CoreData notes appear at the end for the cases where you actually need it.

---

## The Three Pieces of a SwiftData App

Every SwiftData app has three pieces:

- A **model** -- a Swift class annotated with `@Model`. Describes one kind of thing the app stores.
- A **model container** -- the on-disk file and the schema. Declared once, usually on the app's root scene.
- A **model context** -- the working area where objects are created, edited, and saved. SwiftUI provides one automatically through the environment.

### 1. The Model

```swift
import SwiftData

@Model
final class Book {
    var title: String
    var author: String
    var dateAdded: Date
    var isFavorite: Bool

    init(title: String, author: String,
         dateAdded: Date = .now,
         isFavorite: Bool = false) {
        self.title = title
        self.author = author
        self.dateAdded = dateAdded
        self.isFavorite = isFavorite
    }
}
```

The `@Model` macro turns the class into a persistable type. Swift generates the boilerplate to store its properties in the database, track changes, and hand the class to the rest of SwiftData.

Supported property types include `String`, `Int`, `Double`, `Bool`, `Date`, `URL`, `UUID`, `Data`, arrays of those, optionals, other `@Model` classes (as relationships), and your own `Codable` types via `@Attribute`.

### 2. The Model Container

Tell the app what to persist by attaching a container to a scene:

```swift
import SwiftUI
import SwiftData

@main
struct LibraryApp: App {
    var body: some Scene {
        WindowGroup {
            LibraryView()
        }
        .modelContainer(for: Book.self)
    }
}
```

That's all the setup. SwiftData creates the database file under Application Support, migrates the schema if needed, and injects a `ModelContext` into the SwiftUI environment.

Multiple models at once:

```swift
.modelContainer(for: [Book.self, Author.self, Shelf.self])
```

### 3. The Model Context

Inside a view, the context is available via `@Environment`:

```swift
struct AddBookView: View {
    @Environment(\.modelContext) private var context
    @State private var title = ""
    @State private var author = ""

    var body: some View {
        Form {
            TextField("Title",  text: $title)
            TextField("Author", text: $author)
            Button("Save") {
                let book = Book(title: title, author: author)
                context.insert(book)
                // SwiftUI autosaves the context by default.
            }
        }
    }
}
```

`context.insert(_:)` adds the object; `context.delete(_:)` removes it. You rarely call `save()` yourself -- SwiftUI auto-saves between runloop ticks and before the app goes to background.

---

## Fetching Data with @Query

`@Query` is the property wrapper that turns a fetch into a live view binding.

```swift
struct LibraryView: View {
    @Query(sort: \.dateAdded, order: .reverse) private var books: [Book]

    var body: some View {
        List(books) { book in
            VStack(alignment: .leading) {
                Text(book.title).font(.headline)
                Text(book.author).font(.subheadline).foregroundStyle(.secondary)
            }
        }
    }
}
```

`@Query` runs the fetch when the view appears and re-runs it automatically whenever matching data changes. Add a new `Book` anywhere in the app and this list updates without further work.

### Filters

```swift
@Query(filter: #Predicate<Book> { $0.isFavorite },
       sort: \.title)
private var favorites: [Book]
```

`#Predicate` is a freestanding macro that builds a structured, introspectable predicate. You can mix filters, sorts, and fetch limits:

```swift
@Query(filter: #Predicate<Book> { $0.author == "Ada Lovelace" },
       sort:   [SortDescriptor(\.dateAdded, order: .reverse)],
       animation: .default)
private var adaBooks: [Book]
```

---

## Relationships

Models can reference each other. SwiftData handles the relationship tables.

```swift
@Model
final class Author {
    var name: String
    @Relationship(deleteRule: .cascade, inverse: \Book.author)
    var books: [Book] = []

    init(name: String) { self.name = name }
}

@Model
final class Book {
    var title: String
    var author: Author?

    init(title: String, author: Author? = nil) {
        self.title = title
        self.author = author
    }
}
```

`@Relationship(deleteRule: .cascade)` says "when an Author is deleted, delete their Books too." Other options are `.nullify` (set the Book's author to `nil`) and `.deny` (refuse to delete an Author that still has Books).

`inverse:` names the property on the other side. Without it SwiftData doesn't know the two properties describe the same relationship.

---

## Editing Existing Objects

Mutate the object directly. SwiftData notices.

```swift
struct BookRow: View {
    @Bindable var book: Book

    var body: some View {
        HStack {
            TextField("Title", text: $book.title)
            Toggle("Favorite", isOn: $book.isFavorite)
        }
    }
}
```

`@Bindable` makes a `@Model` object into a view-bindable source of truth: you can write `$book.title` and get a SwiftUI `Binding`. Every change saves without extra code.

---

## iCloud Sync

If the container's models are all `Codable` and your app has the **CloudKit** capability enabled, add one modifier:

```swift
.modelContainer(for: Book.self, isAutosaveEnabled: true, isUndoEnabled: true)
```

Actually — for CloudKit sync specifically, you pass a configured `ModelConfiguration`:

```swift
let config = ModelConfiguration(cloudKitDatabase: .automatic)
.modelContainer(for: Book.self, modelConfiguration: config)
```

With CloudKit on, every device signed in to the same Apple ID sees the same data, synced in the background. First-launch sync can take a minute depending on how much data lives in the user's iCloud database; subsequent changes propagate in seconds.

---

## CoreData -- When to Still Reach for It

SwiftData covers most apps. CoreData is still the right pick when:

- You need fine-grained control over the persistent store coordinator, contexts, or performance tuning (batch inserts of tens of thousands of rows, partial object fetching, faulting behavior).
- You are maintaining an app that already has a `.xcdatamodeld` file and migrating to SwiftData would be a large undertaking.
- You need features SwiftData doesn't cover yet, such as denormalized indexes or custom transformable attributes with complex bridging.

CoreData and SwiftData can coexist in the same app: SwiftData's container can point at an existing CoreData store, and you can keep writing through the CoreData API for the old models while using SwiftData for new ones.

---

## Chapter Mini-Example -- Favorites Toggle

```swift
import SwiftUI
import SwiftData

@Model
final class Book {
    var title: String
    var author: String
    var dateAdded: Date
    var isFavorite: Bool

    init(title: String, author: String,
         dateAdded: Date = .now,
         isFavorite: Bool = false) {
        self.title = title
        self.author = author
        self.dateAdded = dateAdded
        self.isFavorite = isFavorite
    }
}

@main
struct LibraryApp: App {
    var body: some Scene {
        WindowGroup { Shelf() }
            .modelContainer(for: Book.self)
    }
}

struct Shelf: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \.dateAdded, order: .reverse) private var books: [Book]

    var body: some View {
        NavigationStack {
            List {
                ForEach(books) { book in
                    Row(book: book)
                }
                .onDelete { indexes in
                    for i in indexes { context.delete(books[i]) }
                }
            }
            .navigationTitle("Library")
            .toolbar {
                Button {
                    context.insert(Book(title: "Untitled",
                                        author: "Anonymous"))
                } label: {
                    Label("Add", systemImage: "plus")
                }
            }
        }
    }
}

struct Row: View {
    @Bindable var book: Book

    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                TextField("Title", text: $book.title)
                    .font(.headline)
                TextField("Author", text: $book.author)
                    .font(.subheadline)
            }
            Spacer()
            Button {
                book.isFavorite.toggle()
            } label: {
                Image(systemName: book.isFavorite ? "star.fill" : "star")
                    .foregroundStyle(book.isFavorite ? .yellow : .secondary)
            }
            .buttonStyle(.plain)
        }
    }
}
```

Rows persist automatically. Deleting swipes a row away and the database is updated. The star button toggles favorite state without any explicit save call. Add CloudKit capability in Xcode (Signing & Capabilities → iCloud → CloudKit) and the library syncs across every device.

---

## What Book 17 Does

Data is now stored and synced. Book 17 turns that data into pictures: Swift Charts for bars, lines, and points, and PDFKit for printable exports.
