# Chapter 11: FileManager and Documents

## FileManager Basics

`FileManager.default` is your entry point for all file system operations. It is a singleton -- use `FileManager.default` everywhere.

### Key Directories

```swift
let fm = FileManager.default

// App's Documents directory (user-visible, backed up to iCloud)
let docs = fm.urls(for: .documentDirectory, in: .userDomainMask).first!

// App's Caches directory (can be purged by system)
let caches = fm.urls(for: .cachesDirectory, in: .userDomainMask).first!

// App's Application Support directory (hidden from user, backed up)
let appSupport = fm.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!

// Temporary directory (purged regularly)
let tmp = fm.temporaryDirectory
```

### The App Sandbox

Every iOS/iPadOS/macOS sandboxed app gets its own container. Your app can only read/write inside its own sandbox without explicit user permission.

The sandbox contains:
- **Documents/** -- User-facing files. Backed up. Visible in Files app if you set `UIFileSharingEnabled` and `LSSupportsOpeningDocumentsInPlace` in Info.plist.
- **Library/Application Support/** -- App data the user doesn't need to see. Backed up.
- **Library/Caches/** -- Recreatable data. Not backed up. System can purge.
- **tmp/** -- Scratch space. Not backed up. Purged between launches.

**Watch out:** On macOS, non-sandboxed apps can access the full filesystem. But App Store apps must be sandboxed. Always code for the sandbox.

---

## Reading and Writing Files

### String I/O

```swift
let fileURL = docs.appendingPathComponent("notes.txt")

// Write
try "Hello, file system".write(to: fileURL, atomically: true, encoding: .utf8)

// Read
let contents = try String(contentsOf: fileURL, encoding: .utf8)
```

`atomically: true` writes to a temp file first, then renames. This prevents corruption if the write is interrupted.

### Data I/O

```swift
let dataURL = docs.appendingPathComponent("photo.jpg")

// Write
try imageData.write(to: dataURL)

// Read
let loaded = try Data(contentsOf: dataURL)
```

### Check If a File Exists

```swift
if fm.fileExists(atPath: fileURL.path) {
    // file is there
}
```

**Watch out:** `fileExists` takes a `String` path, not a `URL`. Use `.path` on the URL. On newer APIs, use `.path()` for the non-deprecated version.

### Create Directories

```swift
let subdir = docs.appendingPathComponent("Exports", isDirectory: true)
try fm.createDirectory(at: subdir, withIntermediateDirectories: true)
```

`withIntermediateDirectories: true` creates parent folders if they don't exist. Like `mkdir -p`.

### Copy, Move, Delete

```swift
// Copy
try fm.copyItem(at: sourceURL, to: destinationURL)

// Move / Rename
try fm.moveItem(at: oldURL, to: newURL)

// Delete
try fm.removeItem(at: fileURL)
```

**Watch out:** All of these throw if the destination already exists (for copy/move) or the source doesn't exist (for delete). Wrap in do-catch.

### List Directory Contents

```swift
let items = try fm.contentsOfDirectory(at: docs, includingPropertiesForKeys: [.isDirectoryKey])
for item in items {
    print(item.lastPathComponent)
}
```

### File Attributes

```swift
let attrs = try fm.attributesOfItem(atPath: fileURL.path)
let size = attrs[.size] as? Int64 ?? 0
let modified = attrs[.modificationDate] as? Date
```

---

## JSON with Codable

The standard pattern for persisting structured data to disk.

### Define Your Model

```swift
struct Project: Codable {
    var name: String
    var version: String
    var tags: [String]
    var lastModified: Date
}
```

### Encode to JSON and Save

```swift
let project = Project(name: "Tally Matrix", version: "3.0", tags: ["tvOS"], lastModified: .now)

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
encoder.dateEncodingStrategy = .iso8601

let data = try encoder.encode(project)
try data.write(to: docs.appendingPathComponent("project.json"))
```

### Load and Decode

```swift
let url = docs.appendingPathComponent("project.json")
let data = try Data(contentsOf: url)

let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601

let project = try decoder.decode(Project.self, from: data)
```

### Common Encoding/Decoding Strategies

```swift
// Dates
encoder.dateEncodingStrategy = .iso8601            // "2026-04-03T12:00:00Z"
encoder.dateEncodingStrategy = .secondsSince1970   // 1775332800.0

// Keys
encoder.keyEncodingStrategy = .convertToSnakeCase  // lastModified -> last_modified
decoder.keyDecodingStrategy = .convertFromSnakeCase
```

### CodingKeys for Custom Mapping

```swift
struct Track: Codable {
    var trackName: String
    var artistName: String
    var durationMs: Int

    enum CodingKeys: String, CodingKey {
        case trackName = "track_name"
        case artistName = "artist_name"
        case durationMs = "duration_ms"
    }
}
```

**Watch out:** Once you define `CodingKeys`, you must list every property you want encoded/decoded. Anything left out is excluded.

---

## PropertyList Encoding

For simpler data that fits the plist format (strings, numbers, dates, booleans, arrays, dictionaries):

```swift
let encoder = PropertyListEncoder()
encoder.outputFormat = .xml // or .binary

let data = try encoder.encode(settings)
try data.write(to: docs.appendingPathComponent("settings.plist"))

let decoder = PropertyListDecoder()
let loaded = try decoder.decode(Settings.self, from: Data(contentsOf: url))
```

JSON is almost always the better choice. Use plist only when interoperating with Apple APIs that expect it.

---

## Security-Scoped Bookmarks

When the user picks a file outside your sandbox (via a file picker), you get temporary access. To keep access across launches, create a bookmark.

### Save a Bookmark

```swift
// After user picks a file via fileImporter
func saveBookmark(for url: URL) throws {
    guard url.startAccessingSecurityScopedResource() else {
        throw FileError.accessDenied
    }
    defer { url.stopAccessingSecurityScopedResource() }

    let bookmarkData = try url.bookmarkData(
        options: .withSecurityScope,
        includingResourceValuesForKeys: nil,
        relativeTo: nil
    )

    // Persist bookmarkData (e.g., in UserDefaults or a file)
    UserDefaults.standard.set(bookmarkData, forKey: "savedFileBookmark")
}
```

### Resolve a Bookmark

```swift
func resolveBookmark() throws -> URL {
    guard let data = UserDefaults.standard.data(forKey: "savedFileBookmark") else {
        throw FileError.noBookmark
    }

    var isStale = false
    let url = try URL(
        resolvingBookmarkData: data,
        options: .withSecurityScope,
        relativeTo: nil,
        bookmarkDataIsStale: &isStale
    )

    if isStale {
        // Re-save the bookmark
        try saveBookmark(for: url)
    }

    guard url.startAccessingSecurityScopedResource() else {
        throw FileError.accessDenied
    }

    return url
    // Caller must call url.stopAccessingSecurityScopedResource() when done
}
```

**Watch out:** Always call `stopAccessingSecurityScopedResource()` when done. The system limits how many security-scoped resources you can access simultaneously.

---

## File Coordination

When multiple processes might access the same file (e.g., your app and an app extension), use `NSFileCoordinator`:

```swift
let coordinator = NSFileCoordinator()
var error: NSError?

coordinator.coordinate(writingItemAt: fileURL, options: [], error: &error) { url in
    try? data.write(to: url)
}

if let error {
    print("Coordination failed: \(error)")
}
```

For reading:

```swift
coordinator.coordinate(readingItemAt: fileURL, options: [], error: &error) { url in
    if let data = try? Data(contentsOf: url) {
        // use data
    }
}
```

**Watch out:** File coordination is mandatory when using shared containers (App Groups). Without it, you risk data corruption when the app and its widget both write to the same file.

---

## UTType (Uniform Type Identifiers)

`UTType` describes file types. Import `UniformTypeIdentifiers`:

```swift
import UniformTypeIdentifiers

let jsonType = UTType.json           // public.json
let pngType = UTType.png             // public.png
let plainText = UTType.plainText     // public.plain-text

// Custom type
extension UTType {
    static let tallyMatrix = UTType(exportedAs: "com.yourapp.tallymatrix")
}

// Check conformance
let type = UTType(filenameExtension: "txt")
type?.conforms(to: .plainText) // true
```

Use `UTType` with file importers/exporters, document types, and drag and drop.

---

## Document-Based Apps

SwiftUI provides `DocumentGroup` for apps centered around file documents.

### FileDocument Protocol

For value-type documents (structs):

```swift
import SwiftUI
import UniformTypeIdentifiers

struct MarkdownDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String

    init(text: String = "") {
        self.text = text
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        text = string
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = text.data(using: .utf8)!
        return FileWrapper(regularFileWithContents: data)
    }
}
```

### ReferenceFileDocument

For reference-type documents (classes), use `ReferenceFileDocument`. This works with `@Observable` or `ObservableObject` classes and supports undo:

```swift
@Observable
class ProjectDocument: ReferenceFileDocument {
    static var readableContentTypes: [UTType] { [.json] }

    var name: String
    var entries: [Entry]

    required init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        let decoded = try JSONDecoder().decode(ProjectData.self, from: data)
        self.name = decoded.name
        self.entries = decoded.entries
    }

    func snapshot(contentType: UTType) throws -> Data {
        try JSONEncoder().encode(ProjectData(name: name, entries: entries))
    }

    func fileWrapper(snapshot: Data, configuration: WriteConfiguration) throws -> FileWrapper {
        FileWrapper(regularFileWithContents: snapshot)
    }
}
```

### DocumentGroup in the App

```swift
@main
struct MyApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MarkdownDocument()) { file in
            TextEditor(text: file.$document.text)
                .font(.body)
        }
    }
}
```

This gives you:
- Open/save dialogs
- File browser on iOS
- Recent documents on macOS
- Autosave
- iCloud document sync (if enabled)

### Registering Document Types

In your target's Info.plist (or via Xcode's Info tab), declare your document types:

- **Exported Type Identifiers** -- for types your app owns
- **Imported Type Identifiers** -- for types defined elsewhere
- **Document Types** -- what your app can open

**Watch out:** If your document type does not appear in the system file picker, your UTType registration is wrong. Double-check the identifier string matches between your `UTType` extension and your Info.plist.

---

## Practical Patterns

### Safe JSON Persistence Manager

```swift
struct PersistenceManager<T: Codable> {
    let fileName: String

    private var fileURL: URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
            .appendingPathComponent(fileName)
    }

    func save(_ value: T) throws {
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        encoder.dateEncodingStrategy = .iso8601
        let data = try encoder.encode(value)
        try data.write(to: fileURL, options: .atomic)
    }

    func load() throws -> T {
        let data = try Data(contentsOf: fileURL)
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(T.self, from: data)
    }

    func delete() throws {
        let fm = FileManager.default
        if fm.fileExists(atPath: fileURL.path) {
            try fm.removeItem(at: fileURL)
        }
    }
}

// Usage
let manager = PersistenceManager<[Project]>(fileName: "projects.json")
try manager.save(projects)
let loaded = try manager.load()
```

### File Importer/Exporter in SwiftUI

```swift
struct ContentView: View {
    @State private var showImporter = false
    @State private var showExporter = false
    @State private var document = MarkdownDocument(text: "Hello")

    var body: some View {
        VStack {
            Button("Import") { showImporter = true }
            Button("Export") { showExporter = true }
        }
        .fileImporter(isPresented: $showImporter, allowedContentTypes: [.plainText]) { result in
            switch result {
            case .success(let url):
                guard url.startAccessingSecurityScopedResource() else { return }
                defer { url.stopAccessingSecurityScopedResource() }
                if let text = try? String(contentsOf: url, encoding: .utf8) {
                    document.text = text
                }
            case .failure(let error):
                print("Import failed: \(error)")
            }
        }
        .fileExporter(isPresented: $showExporter, document: document, contentType: .plainText) { result in
            if case .failure(let error) = result {
                print("Export failed: \(error)")
            }
        }
    }
}
```

**Watch out:** Always call `startAccessingSecurityScopedResource()` on URLs from `fileImporter`. The URL is security-scoped and won't be readable without it.

---

## Quick Reference

| What | How |
|---|---|
| Documents directory | `FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!` |
| Write string to file | `try string.write(to: url, atomically: true, encoding: .utf8)` |
| Read string from file | `try String(contentsOf: url, encoding: .utf8)` |
| Write data to file | `try data.write(to: url)` |
| Read data from file | `try Data(contentsOf: url)` |
| Check file exists | `FileManager.default.fileExists(atPath: url.path)` |
| Create directory | `try fm.createDirectory(at: url, withIntermediateDirectories: true)` |
| Delete file | `try fm.removeItem(at: url)` |
| Encode JSON | `try JSONEncoder().encode(codable)` |
| Decode JSON | `try JSONDecoder().decode(Type.self, from: data)` |
| File document | Conform to `FileDocument` protocol |
| Import file | `.fileImporter(isPresented:allowedContentTypes:)` |
| Export file | `.fileExporter(isPresented:document:contentType:)` |
