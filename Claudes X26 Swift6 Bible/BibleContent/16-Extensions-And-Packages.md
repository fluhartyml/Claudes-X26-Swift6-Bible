# Chapter 16: Extensions & Packages

Your app doesn't have to do everything by itself. Extensions let your app reach outside its own process — into the home screen, the share sheet, Siri, and the lock screen. Packages let you break your code into reusable modules that multiple apps can share. Both are about extending what your app can do without stuffing everything into one target.

## Part 1: App Extensions

### What Is an App Extension?

An app extension is a separate binary that runs outside your app's process. It gets bundled inside your app but lives in its own sandbox. The system launches it when needed — when the user adds your widget to their home screen, shares content to your app, or asks Siri to do something.

The key thing to understand: your extension and your app don't share memory. They're two separate processes. If they need to share data, you have to set that up explicitly through App Groups.

### Widget Extensions (WidgetKit)

Widgets are the most common extension you'll build. They put your app's content on the home screen where the user sees it without opening your app.

A widget has three pieces:

1. **TimelineProvider** — tells the system what to display and when to update
2. **TimelineEntry** — a snapshot of your data at a point in time
3. **Widget View** — the SwiftUI view that renders the entry

```swift
struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> NoteEntry {
        NoteEntry(date: .now, notes: [
            (title: "Sample Note", dateCreated: .now)
        ])
    }

    func getSnapshot(in context: Context,
                     completion: @escaping (NoteEntry) -> Void) {
        completion(fetchEntry())
    }

    func getTimeline(in context: Context,
                     completion: @escaping (Timeline<NoteEntry>) -> Void) {
        let entry = fetchEntry()
        let nextUpdate = Calendar.current.date(
            byAdding: .minute, value: 30, to: .now
        )!
        completion(Timeline(entries: [entry],
                           policy: .after(nextUpdate)))
    }
}
```

The `placeholder` is what the system shows while your widget loads — it should be instant, no data fetching. The `snapshot` is for the widget gallery preview. The `timeline` is the real data.[^1]

### Timeline Policies

The `.after(nextUpdate)` policy tells the system "don't bother refreshing until this time." You're not in control of exactly when your widget refreshes — the system batches updates for battery life. Your policy is a suggestion, not a guarantee.[^2]

Three policies:
- `.atEnd` — refresh after the last entry in the timeline expires
- `.after(date)` — refresh after a specific date
- `.never` — don't refresh until the app tells you to

### Sharing Data with Your App (App Groups)

Your widget runs in a separate process. It can't read your app's SwiftData store directly — unless you put the store in a shared container using App Groups.

The fix is `ModelConfiguration`'s `groupContainer` parameter. Both the app and the widget point at the same App Group identifier, and SwiftData handles the rest:

**Main app (QuickNoteApp.swift):**

```swift
var sharedModelContainer: ModelContainer = {
    let schema = Schema([Note.self])
    let config = ModelConfiguration(
        schema: schema,
        groupContainer: .identifier("group.com.ClaudeX26Bible.QuickNote")
    )
    do {
        return try ModelContainer(for: schema, configurations: [config])
    } catch {
        fatalError("Could not create ModelContainer: \(error)")
    }
}()
```

**Widget extension (QuickNoteWidgetExtension.swift):**

```swift
struct QuickNoteWidgetExtension: Widget {
    let kind: String = "QuickNoteWidgetExtension"

    private let modelContainer: ModelContainer = {
        let config = ModelConfiguration(
            groupContainer: .identifier("group.com.ClaudeX26Bible.QuickNote")
        )
        do {
            return try ModelContainer(for: Note.self, configurations: config)
        } catch {
            fatalError("Widget ModelContainer failed: \(error)")
        }
    }()

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind,
                           provider: Provider(modelContainer: modelContainer)) { entry in
            QuickNoteWidgetEntryView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
    }
}
```

The `ModelContainer` is created once at the Widget struct level and passed into the Provider, so it's reused across all timeline fetches. The Provider uses it to create a `ModelContext` and fetch notes:

```swift
struct Provider: TimelineProvider {
    let modelContainer: ModelContainer

    private func fetchEntry() -> NoteEntry {
        let context = ModelContext(modelContainer)
        let descriptor = FetchDescriptor<Note>(
            sortBy: [SortDescriptor(\.dateCreated, order: .reverse)]
        )
        do {
            let notes = try context.fetch(descriptor)
            let topNotes = notes.prefix(3).map {
                (title: $0.title.isEmpty ? "Untitled" : $0.title,
                 dateCreated: $0.dateCreated)
            }
            return NoteEntry(date: .now, notes: Array(topNotes))
        } catch {
            return NoteEntry(date: .now, notes: [])
        }
    }
}
```

**Setting up the App Group requires three steps:**

1. Register the App Group on developer.apple.com (Identifiers > App Groups > add `group.com.YourTeam.YourApp`)
2. In Xcode, go to Signing & Capabilities for **both** the app target and the widget extension target, add the App Groups capability, and check the group you created
3. Use `groupContainer: .identifier("group.com.YourTeam.YourApp")` in both `ModelConfiguration` instances

Without this, the widget creates its own empty database in its own sandbox and shows "No Notes" — even though the app has data. This was the exact bug we shipped in QuickNote v1.0 and fixed in v1.1.[^3]

To force the widget to refresh when notes change, call `WidgetCenter.shared.reloadAllTimelines()` after any insert, edit, or delete in the main app.

### Creating a Widget Extension Target

In Xcode: **File > New > Target**, then select **Widget Extension** under Application Extension. Give it a product name (convention: YourAppNameWidgetExtension). Xcode creates the target, the boilerplate files, and offers to activate the scheme.

**Important:** The widget's `CFBundleVersion` must match the main app's. If your app is build 3, the widget must be build 3. App Store Connect will reject mismatched versions.

### The Widget View

Widget views are just SwiftUI — but with constraints. No scrolling, no text input, no animations. You get a static snapshot that updates on the timeline schedule.

```swift
struct QuickNoteWidgetEntryView: View {
    var entry: NoteEntry
    @Environment(\.widgetFamily) var family

    var body: some View {
        if entry.notes.isEmpty {
            VStack(spacing: 8) {
                Image(systemName: "note.text")
                    .font(.system(size: 24))
                    .foregroundStyle(.secondary)
                Text("No Notes")
                    .font(.system(size: 16))
                    .foregroundStyle(.secondary)
            }
        } else {
            VStack(alignment: .leading, spacing: 6) {
                ForEach(Array(entry.notes.enumerated()),
                        id: \.offset) { _, note in
                    VStack(alignment: .leading, spacing: 2) {
                        Text(note.title)
                            .font(.system(size: 16, weight: .semibold))
                            .lineLimit(1)
                        Text(dateFormatter.string(from: note.dateCreated)
                            .uppercased())
                            .font(.system(size: 12))
                            .foregroundStyle(.secondary)
                    }
                }
                Spacer(minLength: 0)
            }
            .padding(.vertical, 4)
        }
    }
}
```

Use `@Environment(\.widgetFamily)` to adapt your layout for different sizes — `.systemSmall`, `.systemMedium`, `.systemLarge`.

### Supported Families

```swift
struct QuickNoteWidgetExtension: Widget {
    let kind: String = "QuickNoteWidgetExtension"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            QuickNoteWidgetEntryView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("Recent Notes")
        .description("Shows your most recent notes.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```

The `configurationDisplayName` and `description` are what the user sees in the widget gallery — not the product name from the target settings.

### StaticConfiguration vs AppIntentConfiguration

`StaticConfiguration` — the widget shows the same thing for everyone. No user customization.

`AppIntentConfiguration` — the user can configure the widget (pick which list to show, choose a color, etc.) through the App Intents framework. More powerful, more code.[^4]

Start with `StaticConfiguration`. Add intents when you need them.

### Deep Linking from Widgets

When the user taps your widget, it opens your app. By default it just launches the app. You can use `.widgetURL()` or `Link` to deep link into a specific view.

---

## Part 2: Swift Packages

### What Is a Swift Package?

A Swift Package is a directory with a `Package.swift` manifest and some Swift source files. That's it. No Xcode project file, no storyboards, no asset catalogs. Just code and a manifest.

Packages let you share code between apps without copying files. CryoKit is a package — it defines the data models and station definitions that CryoTunes Player uses. SoundStageKit is another — it provides the shared models, settings, and marker engine that the entire SoundStage suite depends on.

### The Bare Bones Rule

Packages should be data layer only. No fonts, no colors, no aesthetic control. The package provides the engine; the app provides the paint job.

Why? Because two apps using the same package will look different. CryoTunes has a retro blue theme. Tally Matrix has a matrix green theme. If CryoKit set font sizes or colors, one of those apps would look wrong.

The package owns:
- Data models
- Business logic
- Persistence helpers
- Network calls

The app owns:
- Fonts and typography
- Colors and themes
- Layout and spacing
- Platform-specific UI

### Creating a Package

**File > New > Package** in Xcode, or from the command line:

```bash
mkdir MyCoolKit && cd MyCoolKit
swift package init --type library
```

This creates:

```
MyCoolKit/
  Package.swift
  Sources/
    MyCoolKit/
      MyCoolKit.swift
  Tests/
    MyCoolKitTests/
      MyCoolKitTests.swift
```

### Package.swift

The manifest declares your package's name, platforms, products, and dependencies:

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyCoolKit",
    platforms: [
        .iOS(.v17),
        .tvOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "MyCoolKit",
            targets: ["MyCoolKit"]
        ),
    ],
    targets: [
        .target(name: "MyCoolKit"),
        .testTarget(
            name: "MyCoolKitTests",
            dependencies: ["MyCoolKit"]
        ),
    ]
)
```

### Public API

Everything in a package is `internal` by default — invisible to the app that imports it. Mark types, properties, and methods as `public` to expose them:

```swift
public struct Station: Identifiable, Codable, Sendable {
    public let id: UUID
    public let name: String
    public let category: StationCategory

    public init(name: String, category: StationCategory) {
        self.id = UUID()
        self.name = name
        self.category = category
    }
}
```

If you forget `public`, the app will compile but won't be able to see your types. The compiler error is "cannot find type 'Station' in scope" — that usually means you forgot to make it public, not that it doesn't exist.

### Adding a Package to Your App

Two ways:

1. **Local package** — drag the package folder into your Xcode project. Good for development when you're changing the package and the app at the same time.

2. **Remote package** — File > Add Package Dependencies, paste the GitHub URL. Xcode fetches it and pins to a version. This is how you distribute to other developers.

### Versioning

Use semantic versioning — MAJOR.MINOR.PATCH:

- **MAJOR** — breaking changes (removed a public method, changed a type)
- **MINOR** — new features, backwards compatible
- **PATCH** — bug fixes only

Tag your releases in git:

```bash
git tag 1.0.0
git push origin 1.0.0
```

When another developer adds your package, they can pin to a version range like "1.0.0 up to next major" — they get patches and minor updates automatically but won't accidentally pull breaking changes.

### Updating a Package Across Multiple Apps

When you update a package, every app that uses it needs to pull the new version. In Xcode: **File > Packages > Update to Latest Package Versions**.

For local packages, changes appear immediately — no update step needed. That's why local packages are better during active development.

---

## Footnotes

[^1]: Apple Developer Documentation, "Creating a Widget Extension," developer.apple.com/documentation/widgetkit/creating-a-widget-extension. WWDC 2020, "Widgets Code-Along," developer.apple.com/videos/play/wwdc2020/10034/.

[^2]: Apple Developer Documentation, "Keeping a Widget Up To Date," developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date. WWDC 2020, "Widgets Code-Along, Part 3," developer.apple.com/videos/play/wwdc2020/10036/.

[^3]: Apple Developer Documentation, "Configuring App Groups," developer.apple.com/documentation/bundleresources/entitlements/com_apple_security_application-groups. Apple Developer Documentation, "Sharing data with a widget extension," developer.apple.com/documentation/widgetkit/sharing-data-with-your-widget.

[^4]: Apple Developer Documentation, "Making a Configurable Widget," developer.apple.com/documentation/widgetkit/making-a-configurable-widget. WWDC 2023, "Bring Widgets to New Places," developer.apple.com/videos/play/wwdc2023/10027/.
