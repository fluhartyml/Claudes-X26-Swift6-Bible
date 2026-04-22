# Chapter 13: Multi-Window & NavigationSplitView

**Claude's Swift Reference 26** -- Part IV: The Application

---

## What You'll Learn

By the end of this chapter you can:

- Open more than one window of the same app (Mac and iPad).
- Lay out a three-column reader with `NavigationSplitView` that resizes cleanly on iPhone, iPad, and Mac.
- Open, close, and bring windows to the front from code.
- Keep the user's window state across launches so they pick up where they left off.

If you have already built LockBox (Appendix D) or QuickNote (Appendix C), this chapter is the one that teaches them how to grow up into a proper Mac / iPad application with sidebars, detail panes, and multiple open windows.

---

## Scenes, Windows, and the App

Every Apple app has one `App` type as its entry point. Inside it you declare one or more **scenes** -- the top-level containers that SwiftUI manages for you. A scene ends up as a window on Mac and iPad, and as the app's root screen on iPhone.

The simplest app has exactly one scene:

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

`WindowGroup` is the scene type for "a window the user can open more than one of." On Mac, File > New Window opens a second one. On iPad, it takes part in Split View / Slide Over / Stage Manager. On iPhone there is only one window; `WindowGroup` still works, it just never gets a sibling.

### The Other Scene Types

You will meet three other scene types over a typical app's lifetime:

- `Window` -- a single-instance window. Think Preferences on Mac; you don't want two of them open at once.
- `DocumentGroup` -- a scene wired to a file document type. Each open document gets its own window automatically. Covered in Book 11.
- `Settings` -- Mac's Preferences scene. Shows under the app menu as `⌘,`.

For most of this chapter we stay with `WindowGroup`, which covers the common case.

---

## NavigationSplitView -- Sidebar, Content, Detail

`NavigationSplitView` is SwiftUI's answer to the three-column layout you see in Mail, Notes, Files, and every well-built Mac / iPad app. It gives you a sidebar on the left, a content column in the middle, and a detail pane on the right.

### The Two-Column Form

The simplest form has two columns -- sidebar and detail:

```swift
struct Library: View {
    let books = ["Swift in 26 Days", "SwiftUI by Example", "The Pragmatic Programmer"]
    @State private var selected: String?

    var body: some View {
        NavigationSplitView {
            List(books, id: \.self, selection: $selected) { title in
                Text(title)
            }
            .navigationTitle("Library")
        } detail: {
            if let book = selected {
                Text(book)
                    .font(.title)
            } else {
                Text("Select a book")
                    .foregroundStyle(.secondary)
            }
        }
    }
}
```

On iPad and Mac: sidebar and detail appear side by side. On iPhone: the sidebar is the first screen and the detail is pushed when you tap a row.

The `selection:` binding is what makes the detail update when the user picks something in the sidebar. No `NavigationLink` needed.

### The Three-Column Form

When your app has a real hierarchy -- categories, items, item-detail -- reach for the three-column form:

```swift
struct Mailbox: View {
    let folders = ["Inbox", "Sent", "Drafts"]
    @State private var folder: String?
    @State private var messageID: Int?

    var body: some View {
        NavigationSplitView {
            List(folders, id: \.self, selection: $folder) { Text($0) }
                .navigationTitle("Mailboxes")
        } content: {
            if let folder {
                List(1...20, id: \.self, selection: $messageID) { i in
                    Text("\(folder) message #\(i)")
                }
                .navigationTitle(folder)
            } else {
                Text("Pick a mailbox").foregroundStyle(.secondary)
            }
        } detail: {
            if let messageID {
                Text("Message body #\(messageID)").font(.title2)
            } else {
                Text("Pick a message").foregroundStyle(.secondary)
            }
        }
    }
}
```

Three columns on Mac and iPad Pro. Two columns on iPad regular width. Single column pushed through a stack on iPhone. You write the layout once; SwiftUI adapts it to the device.

### columnVisibility -- Controlling What's Open

`NavigationSplitView` takes a binding for **column visibility**. The cases cover the possible states:

- `.all` -- every column visible (only actually shown when there is room).
- `.automatic` -- SwiftUI picks based on size class.
- `.detailOnly` -- sidebar and content hidden, detail takes the whole window.
- `.doubleColumn` -- sidebar hidden, content + detail visible.

The binding lets you drive the UI in code:

```swift
struct Reader: View {
    @State private var columns: NavigationSplitViewVisibility = .automatic

    var body: some View {
        NavigationSplitView(columnVisibility: $columns) {
            sidebar
        } detail: {
            detail
        }
        .toolbar {
            ToolbarItem {
                Button("Focus") { columns = .detailOnly }
            }
        }
    }

    private var sidebar: some View { Text("Sidebar") }
    private var detail: some View { Text("Detail") }
}
```

Tapping Focus hides the sidebar so the reader can concentrate. The system still lets the user reveal it again via edge swipe (iOS) or the default sidebar icon (iPad / Mac).

---

## Opening Extra Windows

On Mac and iPad you can open additional windows of your app's scenes. There are two sides to this: letting the user do it, and doing it in code.

### Letting the User Open Windows

`WindowGroup` already provides this. On Mac, File > New Window appears automatically. On iPad, the user can drag the app's Dock icon to open a second window in Split View. You don't write any code.

### Opening a Window in Code

Use the `openWindow` environment action.

```swift
struct Root: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("New Note Window") {
            openWindow(id: "note")
        }
    }
}
```

For this to work, the scene has to have an `id:` parameter on the `App`:

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup("Library", id: "library") {
            LibraryView()
        }

        WindowGroup("Note", id: "note") {
            NoteView()
        }
    }
}
```

Now `openWindow(id: "note")` creates a new window with a fresh `NoteView`.

### Opening a Window With a Value

If the opened window needs a value -- say, "open this specific note" -- give the scene a `for:` type:

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup("Library") { LibraryView() }

        WindowGroup(for: Note.ID.self) { $noteID in
            if let id = noteID { NoteView(noteID: id) }
        }
    }
}
```

Then open it with a value:

```swift
@Environment(\.openWindow) private var openWindow
// ...
openWindow(value: note.id)
```

Swift picks the `WindowGroup` whose `for:` type matches. The window is restored across launches because the value conforms to `Codable`.

### Dismissing a Window

From inside the window you want to close:

```swift
@Environment(\.dismissWindow) private var dismissWindow

Button("Close") { dismissWindow() }
```

From outside, pass the same `id:` or `value:` you opened with:

```swift
dismissWindow(id: "note")
```

---

## State Restoration

Users expect the app to come back the way they left it -- the same window open, same document, same scroll position. SwiftUI restores most of this automatically as long as you use the right property wrappers.

`@SceneStorage` is the one you reach for most. It's like `@State` except SwiftUI persists it per scene across launches:

```swift
struct NoteView: View {
    @SceneStorage("draft") private var draft = ""
    @SceneStorage("scrollPosition") private var scroll = 0

    var body: some View {
        TextEditor(text: $draft)
    }
}
```

Close the window, relaunch, the text is still there.

For app-wide preferences -- "last-used color scheme," "font size" -- use `@AppStorage` instead; that writes into `UserDefaults` and is shared across every window.

---

## Chapter Mini-Example -- A Two-Window Reader

Putting the pieces together, here is a small app with a library window and a detail window that opens when you click a book.

```swift
import SwiftUI

struct Book: Identifiable, Hashable, Codable {
    let id: Int
    let title: String
}

@main
struct BookShelfApp: App {
    var body: some Scene {
        WindowGroup("Library", id: "library") {
            LibraryView()
        }

        WindowGroup(for: Book.self) { $book in
            if let book = book {
                BookDetailView(book: book)
            }
        }
    }
}

struct LibraryView: View {
    @Environment(\.openWindow) private var openWindow

    private let books = [
        Book(id: 1, title: "Swift in 26 Days"),
        Book(id: 2, title: "SwiftUI by Example"),
        Book(id: 3, title: "The Pragmatic Programmer"),
    ]

    var body: some View {
        NavigationSplitView {
            List(books) { book in
                Button(book.title) { openWindow(value: book) }
                    .buttonStyle(.plain)
            }
            .navigationTitle("Library")
        } detail: {
            Text("Pick a book to open it in its own window.")
                .foregroundStyle(.secondary)
                .padding()
        }
    }
}

struct BookDetailView: View {
    let book: Book
    @SceneStorage("progress") private var progress = 0.0

    var body: some View {
        VStack(alignment: .leading) {
            Text(book.title).font(.largeTitle)
            Slider(value: $progress, in: 0...1)
            Text("Progress: \(Int(progress * 100))%")
        }
        .padding()
        .frame(minWidth: 400, minHeight: 240)
    }
}
```

Clicking a book opens its detail in its own window. The slider position is preserved per-window across launches because `@SceneStorage` is scoped to the scene.

---

## What Book 14 Does

We now have windows we can open, arrange, and restore. Book 14 covers moving content between windows, apps, and devices: clipboard, drag and drop, and share sheets.
