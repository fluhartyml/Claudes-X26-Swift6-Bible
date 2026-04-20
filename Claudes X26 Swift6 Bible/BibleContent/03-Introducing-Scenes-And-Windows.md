# Chapter 3: Introducing Scenes & Windows

**Claude's Swift Bible 26** -- Part I: Introduction

---

## The App Protocol

Every SwiftUI application starts with a struct that conforms to the `App` protocol and is marked `@main`. This is the entry point -- the thing that launches when the user taps your icon.

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

Notice the pattern: `App` has a `body` that returns `some Scene`, just like `View` has a `body` that returns `some View`. The hierarchy goes: **App > Scene > View**.

### Rules of @main

- There is exactly **one** `@main` struct per target. Two `@main` structs in the same target is a compile error.
- The `@main` struct must conform to `App`.
- You initialize app-wide state here (SwiftData containers, shared observable objects, etc.).

### Watch Out For

- If Xcode says "no entry point found," make sure your `App` struct has the `@main` attribute and your file is included in the correct target.
- If you rename your app struct, search for leftover references. The `@main` attribute is what matters, not the struct name.

---

## What a Scene Is

A **Scene** is a container that manages one or more windows. On iOS, you usually have one scene showing one full-screen window. On macOS, scenes can create multiple windows.

Think of it this way:
- **App** -- the process, the thing running in memory
- **Scene** -- a window manager (decides how many windows and what goes in them)
- **View** -- the actual pixels on screen

SwiftUI provides several built-in scene types:

| Scene Type | What It Does | Platforms |
|-----------|-------------|-----------|
| `WindowGroup` | Main app content, supports multiple windows | All |
| `DocumentGroup` | Document-based apps (open/save files) | iOS, macOS |
| `Settings` | Preferences window (Cmd+, on Mac) | macOS only |
| `Window` | A single non-duplicable window | macOS only |
| `MenuBarExtra` | Menu bar item | macOS only |

---

## WindowGroup

`WindowGroup` is the scene type you use 90% of the time. It creates the main window of your app.

```swift
@main
struct TallyMatrixApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Multiple Windows (macOS)

On macOS, `WindowGroup` automatically supports multiple windows. The user can press Cmd+N to open a new window, and each window gets its own independent instance of your content view.

On iOS and iPadOS, `WindowGroup` creates the single main window. On iPadOS, the system may create multiple scenes for Split View / Slide Over, each getting its own instance.

### Window Title and ID

```swift
WindowGroup("Tally Matrix", id: "main") {
    ContentView()
}
```

The string sets the window title on macOS. The `id` lets you distinguish between different window groups if you have more than one.

### Opening Specific Windows (macOS)

If your app has multiple `WindowGroup` scenes, you can open a specific one programmatically:

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup("Main", id: "main") {
            ContentView()
        }

        WindowGroup("Detail", id: "detail", for: Item.ID.self) { $itemID in
            DetailView(itemID: itemID)
        }
    }
}

// From inside a view:
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Open Detail") {
            openWindow(id: "detail", value: selectedItem.id)
        }
        .font(.system(size: 18))
    }
}
```

### Watch Out For

- On macOS, each window from a `WindowGroup` is an independent instance. If they share data, use an `@Observable` object passed through `.environment()`.
- On tvOS, there is always exactly one full-screen window. `WindowGroup` still works; the system just never creates a second window.

---

## DocumentGroup

`DocumentGroup` is for document-based apps -- apps where the user creates, opens, and saves files (like a text editor, image editor, or spreadsheet).

```swift
@main
struct MarkdownEditorApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MarkdownDocument()) { file in
            EditorView(document: file.$document)
        }
    }
}
```

Your document type must conform to `FileDocument` (for value types) or `ReferenceFileDocument` (for reference types).

```swift
struct MarkdownDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String

    init(text: String = "") {
        self.text = text
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8)
        else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.text = string
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = Data(text.utf8)
        return .init(regularFileWithContents: data)
    }
}
```

### Watch Out For

- `DocumentGroup` provides its own navigation (open/save panels on macOS, file browser on iOS). You do not build this UI yourself.
- You must register your document's UTType in Info.plist under `CFBundleDocumentTypes` and `UTExportedTypeDeclarations` (for custom file types) or `UTImportedTypeDeclarations` (for existing types).

---

## Settings Scene (macOS Only)

The `Settings` scene creates the standard Preferences window accessible via Cmd+, (or your app's menu > Settings).

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Settings {
            SettingsView()
        }
    }
}

struct SettingsView: View {
    @AppStorage("refreshInterval") private var refreshInterval = 30
    @AppStorage("showNotifications") private var showNotifications = true

    var body: some View {
        Form {
            Picker("Refresh Interval", selection: $refreshInterval) {
                Text("15 seconds").tag(15)
                Text("30 seconds").tag(30)
                Text("60 seconds").tag(60)
            }
            .font(.system(size: 18))

            Toggle("Show Notifications", isOn: $showNotifications)
                .font(.system(size: 18))
        }
        .formStyle(.grouped)
        .frame(width: 400)
        .padding()
    }
}
```

### Watch Out For

- `Settings` is macOS-only. On iOS, build your settings into the app's UI (a settings tab or gear icon) or use the Settings bundle for system Settings.app integration.
- Do not use `Settings` for critical app configuration. Users expect settings to be optional -- the app should work without ever opening this window.

---

## Window Scene (macOS Only)

`Window` creates a single, non-duplicable window. Unlike `WindowGroup`, the user cannot open a second instance with Cmd+N.

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Window("Activity Log", id: "activity-log") {
            ActivityLogView()
        }
        .keyboardShortcut("L", modifiers: [.command, .shift])
        .defaultSize(width: 600, height: 400)
    }
}
```

Open it from code with `openWindow(id: "activity-log")`.

---

## MenuBarExtra (macOS Only)

`MenuBarExtra` adds an icon to the macOS menu bar. It can show a dropdown menu or a popover-style window.

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star.fill") {
            VStack {
                Text("Status: Running")
                    .font(.system(size: 18))
                Button("Quit") {
                    NSApplication.shared.terminate(nil)
                }
            }
            .padding()
        }
        .menuBarExtraStyle(.window) // .window for a popover, .menu for a dropdown
    }
}
```

### Watch Out For

- A `MenuBarExtra` app with no `WindowGroup` is a "menu bar only" app -- it has no dock icon and no main window. This is intentional for utilities.
- To have both a dock icon and a menu bar presence, include both `WindowGroup` and `MenuBarExtra` in your app body.

---

## App Lifecycle

SwiftUI apps use the `App` protocol's lifecycle. There is no `AppDelegate` by default, though you can add one if needed.

### Scene Phase

SwiftUI provides `scenePhase` to track whether your app is active, inactive, or in the background:

```swift
@main
struct MyApp: App {
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .onChange(of: scenePhase) { oldPhase, newPhase in
            switch newPhase {
            case .active:
                // App is in the foreground and interactive
                break
            case .inactive:
                // App is visible but not interactive (e.g., switching apps)
                break
            case .background:
                // App is not visible -- save data here
                break
            @unknown default:
                break
            }
        }
    }
}
```

### Scene Phase Values

| Phase | Meaning |
|-------|---------|
| `.active` | App is frontmost and receiving input |
| `.inactive` | App is visible but not receiving input (transitioning, notification center open) |
| `.background` | App is not visible (user switched away or locked the screen) |

### When to Use Each Phase

- **Save data** in `.background` -- this is your last chance before the system may terminate your app.
- **Pause timers or animations** in `.inactive`.
- **Resume activity** in `.active`.

### Adding an AppDelegate (When You Need One)

Some things still require an `AppDelegate` (push notification registration, certain third-party SDKs, handling URLs):

```swift
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        // Setup code here
        return true
    }
}

@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

On macOS, use `@NSApplicationDelegateAdaptor` instead.

### Watch Out For

- Do not rely on `scenePhase` for saving critical data on tvOS. tvOS apps can be terminated without warning. Save continuously or after each user action.
- `scenePhase` on macOS applies per-scene (per-window), not per-app. Closing one window does not mean the app is backgrounded if another window is open.

---

## Multi-Platform Considerations

SwiftUI's promise is "write once, adapt everywhere." The reality is close but requires awareness of platform differences.

### iOS / iPadOS

- **One WindowGroup**, one full-screen window (iPadOS supports multitasking with multiple scenes).
- **No Settings scene** -- build settings into your app's UI.
- Navigation typically uses `NavigationStack` or `NavigationSplitView`.
- System bars: status bar at top, home indicator at bottom. Use `.ignoresSafeArea()` carefully.

### macOS

- **Multiple windows** are the norm. Each `WindowGroup` window is independent.
- **Settings scene** via Cmd+,.
- **Menu bar** is important. SwiftUI generates a default menu; customize with `.commands()`.
- **Window sizing**: use `.defaultSize()`, `.frame(minWidth:maxWidth:)` on the content view.

```swift
WindowGroup {
    ContentView()
        .frame(minWidth: 600, minHeight: 400)
}
.defaultSize(width: 800, height: 600)
```

### tvOS

- **Full-screen only.** One window, no resizing, no multitasking.
- **Focus-based navigation.** No touch -- users navigate with the Siri Remote. See Chapter 4 for focus system details.
- **10-foot UI.** Everything must be large and readable from across the room. Your 18pt minimum is a *floor*, not a target -- consider 28pt+ for main content on TV.
- No `Settings` scene, no `MenuBarExtra`.

### visionOS

- **Windows float in space.** `WindowGroup` creates a 2D window in the user's environment.
- **Volumes**: use `.windowStyle(.volumetric)` for 3D content in a bounded box.
- **Immersive spaces**: `ImmersiveSpace` scene type for full 3D environments.
- Eyes and hands replace touch. Standard SwiftUI controls work automatically with gaze-and-tap.

```swift
@main
struct MyVisionApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .defaultSize(width: 600, height: 400, depth: 0, in: .points)

        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
    }
}
```

### watchOS

- **Single view, small screen.** Focus on glanceable information.
- `NavigationStack` with simple lists is the standard pattern.
- Digital Crown input via `.digitalCrownRotation()`.

---

## Conditional Compilation for Platforms

When you need platform-specific code:

```swift
var body: some Scene {
    WindowGroup {
        ContentView()
    }

    #if os(macOS)
    Settings {
        SettingsView()
    }
    #endif
}
```

Available compile-time checks:

| Check | Matches |
|-------|---------|
| `#if os(iOS)` | iPhone and iPad |
| `#if os(macOS)` | Mac |
| `#if os(tvOS)` | Apple TV |
| `#if os(watchOS)` | Apple Watch |
| `#if os(visionOS)` | Apple Vision Pro |
| `#if targetEnvironment(simulator)` | Running in simulator |
| `#if canImport(UIKit)` | UIKit is available (iOS, tvOS, visionOS) |
| `#if canImport(AppKit)` | AppKit is available (macOS) |

### Watch Out For

- `os(iOS)` matches both iPhone and iPad. Use `UIDevice.current.userInterfaceIdiom == .pad` at runtime to distinguish (but prefer adaptive layout over device checks).
- Mac Catalyst apps match `os(iOS)`, not `os(macOS)`. Use `#if targetEnvironment(macCatalyst)` to detect Catalyst specifically.
- Overusing `#if os(...)` makes code hard to maintain. Prefer designing views that adapt naturally with `GeometryReader`, `ViewThatFits`, or `NavigationSplitView`'s automatic collapsing behavior.

---

## Combining Multiple Scenes

A real-world macOS app might combine several scene types:

```swift
@main
struct ProductivityApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup("Documents", id: "documents") {
            DocumentBrowser()
                .environment(appState)
        }
        .commands {
            SidebarCommands()
            ToolbarCommands()
        }

        Window("Quick Note", id: "quick-note") {
            QuickNoteView()
                .environment(appState)
        }
        .keyboardShortcut("N", modifiers: [.command, .shift])
        .defaultSize(width: 400, height: 300)

        Settings {
            SettingsView()
                .environment(appState)
        }

        MenuBarExtra("Quick Access", systemImage: "note.text") {
            MenuBarView()
                .environment(appState)
        }
        .menuBarExtraStyle(.window)
    }
}
```

Pass shared `@Observable` state through `.environment()` so all scenes can access the same data.

---

## Practical Tips

1. **Start with one WindowGroup.** You can add Settings, MenuBarExtra, and extra windows later. Do not over-architect the scene structure before you need it.

2. **Test your macOS app with multiple windows early.** Open two windows and make sure they do not fight over shared state. This catches bugs that are invisible in single-window testing.

3. **Save in `.background`, not just on button tap.** Users force-quit apps, phones run out of battery, systems terminate background apps. The `.background` scene phase is your safety net.

4. **Use `.defaultSize()` on macOS windows.** Without it, SwiftUI guesses a size based on content, which is often wrong.

5. **On tvOS, do not fight the focus system.** SwiftUI handles focus automatically for standard controls. Custom focus behavior is covered in Chapter 4.

6. **Keep your App struct thin.** Initialize state, define scenes, and stop. Business logic belongs in your model layer, not in the `App` body.

---

*Claude's Swift Bible 26 -- Chapter 3*
*Written by Claude for Michael Fluharty. Swift 6, Xcode 26.*
