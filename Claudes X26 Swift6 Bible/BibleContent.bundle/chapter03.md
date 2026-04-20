# Chapter 3: Introducing Scenes and Windows

*Claude's Xcode 26 Swift Bible — Part I: Introduction*

---

## 1. The App Protocol

1.1 Every SwiftUI app starts with a struct <<Glossary: Struct>> that conforms to the `App` protocol and is marked `@main`. This is the entry point — the thing that launches when the user taps your icon.

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

1.2 Notice the pattern: `App` has a `body` that returns `some Scene`, just like `View` has a `body` that returns `some View` <<Glossary: View>>. The hierarchy goes: **App > Scene > View**. The app is the process running in memory. The scene manages windows. The views are the actual pixels on screen.

1.3 **Rules of @main:**
1) There is exactly one `@main` struct per target <<Glossary: Target>>. Two `@main` structs in the same target is a compile error.
2) The `@main` struct must conform to `App`.
3) This is where you initialize app-wide state — SwiftData containers, shared observable objects, anything the whole app needs access to.

1.4 **Watch out:** If Xcode says "no entry point found," make sure your App struct has the `@main` attribute and the file is included in the correct target (check Target Membership in the right sidebar). If you rename your app struct, search for leftover references — the `@main` attribute is what matters, not the struct name.

---

## 2. What a Scene Is

2.1 A **Scene** is a container that manages one or more windows. Think of it this way:
- **App** — the process, the thing running in memory
- **Scene** — the window manager (decides how many windows and what goes in them)
- **View** — the actual stuff on screen

2.2 On iPhone, you usually have one scene showing one full-screen window. On Mac, scenes can create multiple windows. On Apple TV, there's always one full-screen window.

2.3 SwiftUI gives you several built-in scene types:
- **WindowGroup** — main app content, supports multiple windows. Used 90% of the time. Works on all platforms.
- **DocumentGroup** — for document-based apps where the user creates, opens, and saves files. iOS and macOS.
- **Settings** — the Preferences window on Mac (Cmd+,). macOS only.
- **Window** — a single window that can't be duplicated with Cmd+N. macOS only.
- **MenuBarExtra** — an icon in the Mac menu bar with a dropdown or popover. macOS only.

---

## 3. WindowGroup

3.1 `WindowGroup` is the scene you'll use in almost every app. It creates the main window.

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

3.2 **On macOS**, `WindowGroup` automatically supports multiple windows. The user presses Cmd+N and gets a new window — each one is an independent instance of your content view. **On iOS**, it creates the single main window. **On iPadOS**, the system may create multiple scenes for Split View or Slide Over. **On tvOS**, there's always exactly one full-screen window.

3.3 You can give the window a title and an ID:

```swift
WindowGroup("Tally Matrix", id: "main") {
    ContentView()
}
```

3.4 The string sets the window title on macOS. The `id` lets you tell windows apart if you have more than one `WindowGroup`.

3.5 **Watch out:** On macOS, each window from a `WindowGroup` is independent. If they need to share data, use an `@Observable` object passed through `.environment()`. Otherwise each window has its own separate copy of everything.

---

## 4. DocumentGroup

4.1 `DocumentGroup` is for apps where the user creates, opens, and saves files — a text editor, an image editor, a spreadsheet. You probably won't need this for most apps, but it's here when you do.

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

4.2 Your document type must conform to `FileDocument` (for value types) or `ReferenceFileDocument` (for reference types). The document protocol handles reading and writing the file — you tell it what file type it supports and how to convert between your data and the file's bytes.

4.3 **Watch out:** `DocumentGroup` provides its own navigation — open/save panels on macOS, file browser on iOS. You don't build that UI yourself. You also need to register your document's file type in Info.plist <<Glossary: Info.plist>> under `CFBundleDocumentTypes`.

---

## 5. Settings Scene (macOS Only)

5.1 The `Settings` scene creates the standard Preferences window that opens when the user presses Cmd+, or goes to your app's menu > Settings.

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
```

5.2 This only works on macOS. On iOS, you build your settings into the app's UI — a settings tab, a gear icon, or a dedicated screen. There is no system-level settings scene on iPhone or iPad.

5.3 **Watch out:** Don't use Settings for anything critical. Users expect the app to work without ever opening this window. It's for preferences, not configuration.

---

## 6. Window and MenuBarExtra (macOS Only)

6.1 **Window** creates a single window that can't be duplicated. Unlike `WindowGroup`, the user can't press Cmd+N to open another one. Good for things like an activity log or an inspector panel.

```swift
Window("Activity Log", id: "activity-log") {
    ActivityLogView()
}
.keyboardShortcut("L", modifiers: [.command, .shift])
.defaultSize(width: 600, height: 400)
```

6.2 Open it from code with `openWindow(id: "activity-log")`.

6.3 **MenuBarExtra** adds an icon to the macOS menu bar — the row of icons at the top right of your screen. It can show a dropdown menu or a small popover window.

```swift
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
.menuBarExtraStyle(.window)
```

6.4 A `MenuBarExtra` app with no `WindowGroup` is a "menu bar only" app — no dock icon, no main window. Just the icon in the menu bar. That's intentional for utilities. To have both a dock icon and a menu bar presence, include both `WindowGroup` and `MenuBarExtra` in your app body.

---

## 7. App Lifecycle

7.1 SwiftUI tracks whether your app is active, inactive, or in the background using `scenePhase`. This matters because you need to know when to save data — the system can terminate your app without warning when it's in the background.

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
                // App is visible but not interactive (switching apps, notification center open)
                break
            case .background:
                // App is not visible — save data here
                break
            @unknown default:
                break
            }
        }
    }
}
```

7.2 **The three phases:**
- **.active** — app is frontmost and receiving input. The user is using it right now.
- **.inactive** — app is visible but not receiving input. Happens briefly when switching apps or when the notification center slides down.
- **.background** — app is not visible. The user switched away or locked the screen. This is your last chance to save data before the system may kill your app.

7.3 **When to use each:** Save data in `.background`. Pause timers or animations in `.inactive`. Resume activity in `.active`.

7.4 **AppDelegate — when you still need one.** Some things still require the old-school AppDelegate — push notification registration, certain third-party SDKs, handling URLs. You can bridge it in:

```swift
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
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

On macOS, use `@NSApplicationDelegateAdaptor` instead of `@UIApplicationDelegateAdaptor`.

7.5 **Watch out:** Don't rely on `scenePhase` alone for saving critical data on tvOS — tvOS apps can be terminated without warning. Save continuously or after each user action. On macOS, `scenePhase` applies per-window, not per-app — closing one window doesn't mean the app is backgrounded if another window is still open.

---

## 8. Multi-Platform Considerations

8.1 SwiftUI's promise is "write once, adapt everywhere." The reality is close but requires awareness of how each platform behaves differently.

8.2 **iOS / iPadOS:**
- One `WindowGroup`, one full-screen window (iPadOS supports multitasking with multiple scenes)
- No `Settings` scene — build settings into your app's UI
- Navigation uses `NavigationStack` or `NavigationSplitView`
- Status bar at top, home indicator at bottom — be careful with `.ignoresSafeArea()`

8.3 **macOS:**
- Multiple windows are the norm — each `WindowGroup` window is independent
- `Settings` scene via Cmd+,
- Menu bar matters — SwiftUI generates a default one, customize with `.commands()`
- Set window sizes with `.defaultSize()` on the scene and `.frame(minWidth:maxWidth:)` on the content view

8.4 **tvOS:**
- Full-screen only. One window, no resizing, no multitasking.
- Focus-based navigation — no touch, users navigate with the Siri Remote. Chapter 4 covers the focus system.
- 10-foot UI — everything must be readable from across the room. The 18pt minimum is a floor, not a target. Consider 28pt+ for main content on TV.

8.5 **visionOS:**
- Windows float in space. `WindowGroup` creates a 2D window in the user's environment.
- Volumes (`.windowStyle(.volumetric)`) for 3D content in a bounded box.
- `ImmersiveSpace` scene type for full 3D environments.
- Eyes and hands replace touch. Standard SwiftUI controls work automatically with gaze-and-tap.

8.6 **watchOS:**
- Single view, small screen. Focus on glanceable information.
- `NavigationStack` with simple lists is the standard pattern.
- Digital Crown input via `.digitalCrownRotation()`.

---

## 9. Conditional Compilation

9.1 When you need code that only runs on a specific platform, use `#if os(...)`:

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

9.2 **Available checks:**
- `#if os(iOS)` — iPhone and iPad
- `#if os(macOS)` — Mac
- `#if os(tvOS)` — Apple TV
- `#if os(watchOS)` — Apple Watch
- `#if os(visionOS)` — Apple Vision Pro
- `#if targetEnvironment(simulator)` — running in a simulator
- `#if canImport(UIKit)` — UIKit is available (iOS, tvOS, visionOS)
- `#if canImport(AppKit)` — AppKit is available (macOS)

9.3 **Watch out:** `os(iOS)` matches both iPhone and iPad. Use `UIDevice.current.userInterfaceIdiom == .pad` at runtime to distinguish, but prefer adaptive layout over device checks. Mac Catalyst apps match `os(iOS)`, not `os(macOS)` — use `#if targetEnvironment(macCatalyst)` to detect Catalyst specifically. And don't overuse `#if os(...)` — it makes code hard to maintain. Prefer views that adapt naturally.

---

## 10. Tips

10.1 **Start with one WindowGroup.** You can add Settings, MenuBarExtra, and extra windows later. Don't over-architect the scene structure before you need it.

10.2 **Test macOS apps with multiple windows early.** Open two windows and make sure they don't fight over shared state. This catches bugs that are invisible in single-window testing.

10.3 **Save in `.background`, not just on button tap.** Users force-quit apps, phones run out of battery, systems terminate background apps. The `.background` scene phase is your safety net.

10.4 **Use `.defaultSize()` on macOS windows.** Without it, SwiftUI guesses a size based on content, which is often wrong.

10.5 **On tvOS, don't fight the focus system.** SwiftUI handles focus automatically for standard controls. Custom focus behavior is covered in Chapter 4.

10.6 **Keep your App struct thin.** Initialize state, define scenes, and stop. Business logic belongs in your model layer, not in the `App` body.

---

*Claude's Xcode 26 Swift Bible — Chapter 3*
*By Dr. Wahl — co-authored by Claude A. and Michael Fluharty. Swift 6, Xcode 26.*
