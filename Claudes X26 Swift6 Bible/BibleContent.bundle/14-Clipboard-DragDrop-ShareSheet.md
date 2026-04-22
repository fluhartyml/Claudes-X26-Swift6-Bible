# Chapter 14: Clipboard, Drag & Drop, Share Sheet

**Claude's Swift Reference 26** -- Part IV: The Application

---

## What You'll Learn

By the end of this chapter you can:

- Read from and write to the system clipboard on iOS and macOS.
- Make your own types participate in copy / paste, drag / drop, and the share sheet via one protocol: `Transferable`.
- Let the user drag content between views in your app and between your app and other apps.
- Present the system share sheet so users can send content to Messages, Mail, AirDrop, and the rest.

These are the three ways Apple platforms move data between places. Once you have them, every app that handles user content feels like a native citizen.

---

## Transferable -- One Protocol Covers All Three

`Transferable` is the unifying protocol. A type that conforms to `Transferable` can be copied to the clipboard, dragged from one view to another, and handed to the share sheet -- all through the same API. If your data type conforms to `Codable`, the conformance is often a single line.

```swift
import CoreTransferable

struct Note: Codable, Transferable {
    let title: String
    let body: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .json)
    }
}
```

`CodableRepresentation` is a built-in representation that encodes the type as JSON under the given Uniform Type Identifier (UTI). Now `Note` can cross every data-movement boundary SwiftUI understands.

For plain-text or image types you usually don't define a custom `Transferable`. `String`, `URL`, `Data`, `Image`, and `UIImage` / `NSImage` already conform.

---

## The Clipboard (Copy and Paste)

### Writing to the Clipboard

iOS uses `UIPasteboard.general`; macOS uses `NSPasteboard.general`. SwiftUI hides the platform split for simple cases with `Button` styles that target copying, but you'll often write directly.

```swift
#if os(iOS)
import UIKit

func copy(_ text: String) {
    UIPasteboard.general.string = text
}
#else
import AppKit

func copy(_ text: String) {
    NSPasteboard.general.clearContents()
    NSPasteboard.general.setString(text, forType: .string)
}
#endif
```

Plain text is the simplest case. Writing an image:

```swift
// iOS
UIPasteboard.general.image = UIImage(systemName: "heart")
```

### Reading from the Clipboard

```swift
#if os(iOS)
let text = UIPasteboard.general.string ?? ""
#else
let text = NSPasteboard.general.string(forType: .string) ?? ""
#endif
```

### Built-In Copy / Paste UI

On iOS, every `TextField` and `TextEditor` already shows a copy / paste menu when the user taps and holds. You don't wire that up. Where you DO wire it up is on non-text content -- a card view, an image tile -- via the `.contextMenu`:

```swift
Image("kitten")
    .contextMenu {
        Button {
            UIPasteboard.general.image = UIImage(named: "kitten")
        } label: {
            Label("Copy Image", systemImage: "doc.on.doc")
        }
    }
```

---

## Drag and Drop

### Making a View Draggable

Attach `.draggable` with a `Transferable` value:

```swift
struct Card: View {
    let note: Note

    var body: some View {
        Text(note.title)
            .padding()
            .background(.yellow)
            .draggable(note)
    }
}
```

That's it. On Mac the card now drags with a normal mouse. On iPad the user presses and lifts with a finger or Apple Pencil. The drag preview uses the view itself.

You can provide a custom preview:

```swift
Text(note.title)
    .draggable(note) {
        RoundedRectangle(cornerRadius: 8)
            .fill(.yellow)
            .frame(width: 80, height: 40)
            .overlay(Text(note.title).font(.caption))
    }
```

### Accepting a Drop

Attach `.dropDestination` to the view that should receive drops:

```swift
struct Trash: View {
    @State private var count = 0

    var body: some View {
        Image(systemName: "trash")
            .font(.largeTitle)
            .padding()
            .dropDestination(for: Note.self) { notes, _ in
                count += notes.count
                return true
            }
            .overlay(alignment: .topTrailing) {
                if count > 0 { Text("\(count)").padding(4).background(.red) }
            }
    }
}
```

The closure gets an array of the dropped values (multiple items can drop at once) plus a `CGPoint` location in the view's coordinates. Return `true` to accept the drop, `false` to refuse.

### Highlighting While Hovering

`.dropDestination` takes an `isTargeted:` binding that flips to `true` while something draggable is hovering over the view:

```swift
@State private var hovering = false

Image(systemName: "tray")
    .padding()
    .background(hovering ? .blue.opacity(0.2) : .clear)
    .dropDestination(for: Note.self) { notes, _ in
        return true
    } isTargeted: { hovering = $0 }
```

### Inter-App Drag on iPadOS

Because `Transferable` types also declare their UTI, a drag that leaves your app -- onto another app or into Files -- can still be accepted if the destination understands the UTI. Drag a note with `.json` type into Files and you get a `.json` file written there. Drag a plain `String` into Messages and it becomes a chat bubble. The system does the dispatch; you do nothing extra.

---

## The Share Sheet

The share sheet is the system UI for "send this content somewhere": Messages, Mail, AirDrop, Notes, copy, and any app that registered a share extension.

### SwiftUI's ShareLink

Most of the time you'll use `ShareLink`, which is to sharing what `Button` is to actions:

```swift
ShareLink(item: "Hello from the book") {
    Label("Share", systemImage: "square.and.arrow.up")
}
```

The label is optional; without one, `ShareLink` renders a default share glyph. `ShareLink` accepts any `Transferable`:

```swift
ShareLink(item: note,
          preview: SharePreview(note.title,
                                icon: Image(systemName: "note.text")))
```

`SharePreview` supplies the tiny preview that shows up at the top of the share sheet (the AirDrop card, the header in Messages, etc.).

### Multiple Items

```swift
let urls: [URL] = [photoOne, photoTwo, photoThree]
ShareLink(items: urls) { Label("Share Photos", systemImage: "photo") }
```

### Triggering the Share Sheet Manually (UIKit / AppKit)

Sometimes you want the share sheet to open in response to a custom gesture, not a button. Use `UIActivityViewController` on iOS:

```swift
#if os(iOS)
func share(_ items: [Any]) {
    guard let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
          let root  = scene.windows.first?.rootViewController else { return }

    let vc = UIActivityViewController(activityItems: items, applicationActivities: nil)
    root.present(vc, animated: true)
}
#endif
```

On Mac, `NSSharingServicePicker` does the same job.

---

## Chapter Mini-Example -- Cards You Can Copy, Drag, or Share

```swift
import SwiftUI
import CoreTransferable

struct Note: Codable, Identifiable, Transferable {
    let id = UUID()
    var title: String
    var body: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .json)
    }
}

struct CardBoard: View {
    @State private var notes: [Note] = [
        Note(title: "Milk", body: "2%, gallon"),
        Note(title: "Bread", body: "Sourdough"),
        Note(title: "Kale", body: "For the smoothie")
    ]

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                ForEach(notes) { note in
                    NoteCard(note: note)
                }
            }
            .padding()
        }
    }
}

struct NoteCard: View {
    let note: Note
    @State private var hovering = false

    var body: some View {
        VStack(alignment: .leading) {
            Text(note.title).font(.headline)
            Text(note.body).font(.subheadline)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(hovering ? .yellow.opacity(0.5) : .yellow.opacity(0.2))
        .cornerRadius(10)
        .contextMenu {
            Button("Copy Title") {
                #if os(iOS)
                UIPasteboard.general.string = note.title
                #else
                NSPasteboard.general.clearContents()
                NSPasteboard.general.setString(note.title, forType: .string)
                #endif
            }
            ShareLink(item: note,
                      preview: SharePreview(note.title,
                                            icon: Image(systemName: "note.text")))
        }
        .draggable(note)
        .dropDestination(for: Note.self) { incoming, _ in
            return true
        } isTargeted: { hovering = $0 }
    }
}
```

Each card can be copied from its context menu, dragged onto another card, and shared through the system share sheet. Users can also drag cards out to Files or Messages because `Note` carries a JSON UTI.

---

## What Book 15 Does

Book 14 moved data between views and apps. Book 15 covers where data lives when the app isn't running: SwiftData and CoreData for on-device storage, with optional CloudKit sync between devices.
