# Chapter 07: Toolbars and Tab Views

## The .toolbar Modifier

The `.toolbar` modifier is the single entry point for adding buttons, menus, and controls to navigation bars, bottom bars, and keyboard accessories.

```swift
struct ItemListView: View {
    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        .navigationTitle("Items")
        .toolbar {
            Button("Add", systemImage: "plus") {
                addItem()
            }
        }
    }
}
```

Without specifying a placement, the system puts the button where it makes sense for the platform — trailing on iOS, trailing in the toolbar on macOS.

---

## ToolbarItem

Use `ToolbarItem` when you need to control exactly where a button lands.

```swift
.toolbar {
    ToolbarItem(placement: .primaryAction) {
        Button("Save") { save() }
    }

    ToolbarItem(placement: .cancellationAction) {
        Button("Cancel") { dismiss() }
    }

    ToolbarItem(placement: .destructiveAction) {
        Button("Delete", role: .destructive) { delete() }
    }
}
```

---

## ToolbarItemGroup

Group multiple items in the same placement.

```swift
.toolbar {
    ToolbarItemGroup(placement: .primaryAction) {
        Button("Share", systemImage: "square.and.arrow.up") { share() }
        Button("Edit", systemImage: "pencil") { edit() }
        Button("Add", systemImage: "plus") { add() }
    }
}
```

---

## Toolbar Placements

### Semantic Placements (Preferred)

These let the system decide the exact position based on platform conventions.

| Placement | iOS | macOS | Use For |
|-----------|-----|-------|---------|
| `.automatic` | Trailing nav bar | Toolbar area | Default, system decides |
| `.primaryAction` | Trailing nav bar | Trailing toolbar | Main action (Save, Add) |
| `.secondaryAction` | Overflow menu | Toolbar customization | Less-used actions |
| `.cancellationAction` | Leading nav bar | Leading toolbar | Cancel/Dismiss |
| `.confirmationAction` | Trailing nav bar | Trailing toolbar | Confirm/Done in sheets |
| `.destructiveAction` | Trailing nav bar | Trailing toolbar | Delete/Remove |
| `.navigation` | Leading nav bar | Leading toolbar | Back-like navigation |

### Positional Placements

| Placement | Where |
|-----------|-------|
| `.topBarLeading` | iOS: left side of nav bar |
| `.topBarTrailing` | iOS: right side of nav bar |
| `.bottomBar` | iOS: bottom bar above tab bar |
| `.keyboard` | iOS: above the keyboard |
| `.tabBar` | Inside the tab bar area |

### Bottom Bar

```swift
.toolbar {
    ToolbarItemGroup(placement: .bottomBar) {
        Button("Previous", systemImage: "chevron.left") { previous() }
        Spacer()
        Text("Page \(currentPage) of \(totalPages)")
        Spacer()
        Button("Next", systemImage: "chevron.right") { next() }
    }
}
```

### Keyboard Toolbar

Add a "Done" button above the keyboard. Essential for dismissing number pads and other keyboards that lack a return key.

```swift
TextField("Amount", value: $amount, format: .number)
    .keyboardType(.decimalPad)
    .toolbar {
        ToolbarItemGroup(placement: .keyboard) {
            Spacer()
            Button("Done") {
                isFocused = false
            }
        }
    }
```

### Watch Out

- `.keyboard` placement only shows when the keyboard is visible. If you have multiple text fields, the keyboard toolbar is shared — whichever field is focused gets it.
- `.bottomBar` does not appear if the view is inside a `TabView`. The tab bar occupies that space. Use `.tabBar` placement instead if you need items alongside tabs.

---

## Toolbar Visibility

Hide or show toolbars explicitly.

```swift
.toolbar(.hidden, for: .navigationBar)    // hide the nav bar
.toolbar(.visible, for: .bottomBar)       // force bottom bar visible
.toolbar(.hidden, for: .tabBar)           // hide tab bar (e.g., in detail views)
```

The `for:` parameter targets: `.navigationBar`, `.bottomBar`, `.tabBar`, `.windowToolbar` (macOS).

### Watch Out

- Hiding `.tabBar` only works from a view inside a `TabView`. If you hide it from outside the tab hierarchy, nothing happens.
- Use `.toolbar(.hidden, for: .tabBar)` on detail views where you want a full-screen experience. It animates smoothly.

---

## Toolbar on macOS vs iOS

### macOS-Specific Toolbar Style

```swift
WindowGroup {
    ContentView()
}
.windowToolbarStyle(.unified)           // toolbar merges with title bar
.windowToolbarStyle(.unifiedCompact)    // thinner merged toolbar
.windowToolbarStyle(.expanded)          // toolbar below title bar
```

### macOS Toolbar Customization

Users can customize the macOS toolbar by default. To control what is customizable:

```swift
.toolbar(id: "main") {
    ToolbarItem(id: "add", placement: .primaryAction) {
        Button("Add", systemImage: "plus") { }
    }
    ToolbarItem(id: "share", placement: .secondaryAction) {
        Button("Share", systemImage: "square.and.arrow.up") { }
    }
}
.toolbarRole(.editor)  // changes toolbar behavior and appearance
```

### Watch Out

- On macOS, `.primaryAction` items are always visible. `.secondaryAction` items go into the customization palette and may be hidden by default.
- `ToolbarItem(id:)` requires a stable string identifier for toolbar customization persistence. Without IDs, user customizations are lost between launches.

---

## TabView In Depth

### Basic Tab Setup

```swift
struct RootView: View {
    @State private var selectedTab: AppTab = .home

    var body: some View {
        TabView(selection: $selectedTab) {
            Tab("Home", systemImage: "house", value: .home) {
                NavigationStack {
                    HomeView()
                }
            }

            Tab("Library", systemImage: "books.vertical", value: .library) {
                NavigationStack {
                    LibraryView()
                }
            }

            Tab("Profile", systemImage: "person", value: .profile) {
                NavigationStack {
                    ProfileView()
                }
            }
        }
    }
}

enum AppTab: Hashable {
    case home, library, profile
}
```

### Badge Modifier

```swift
Tab("Inbox", systemImage: "tray", value: .inbox) {
    InboxView()
}
.badge(unreadCount)     // integer badge
.badge("New")           // text badge
```

Badges appear as a small indicator on the tab icon. On iOS, it is a red circle with the count. On macOS, it is a text overlay.

### Tab Sections (iPadOS / visionOS Sidebar)

On iPadOS with sufficient width, `TabView` can render as a sidebar. Group tabs with `TabSection`.

```swift
TabView {
    Tab("Home", systemImage: "house", value: .home) {
        HomeView()
    }

    TabSection("Library") {
        Tab("Books", systemImage: "book", value: .books) {
            BooksView()
        }
        Tab("Audiobooks", systemImage: "headphones", value: .audiobooks) {
            AudiobooksView()
        }
    }

    TabSection("Account") {
        Tab("Profile", systemImage: "person", value: .profile) {
            ProfileView()
        }
        Tab("Settings", systemImage: "gear", value: .settings) {
            SettingsView()
        }
    }
}
.tabViewStyle(.sidebarAdaptable)
```

### Page-Style TabView

For swipeable pages (onboarding, image galleries).

```swift
TabView {
    OnboardingPage1()
    OnboardingPage2()
    OnboardingPage3()
}
.tabViewStyle(.page)
.indexViewStyle(.page(backgroundDisplayMode: .always))
```

### Watch Out

- Each tab should own its own `NavigationStack`. Wrapping the entire `TabView` in a single `NavigationStack` causes the nav bar to appear above tabs and navigation pushes replace the whole tab interface.
- `.tabViewStyle(.page)` hides the tab bar entirely. It shows dots instead. Do not mix page style with labeled tabs.
- Tab order is the order you declare them. There is no reordering API like UIKit's "More" tab — though the sidebar-adaptable style on iPad does support reordering.

---

## Custom Tab Bar

When the built-in tab bar does not meet your needs, build your own.

```swift
struct CustomTabBar: View {
    @Binding var selectedTab: AppTab

    var body: some View {
        HStack {
            ForEach(AppTab.allCases, id: \.self) { tab in
                Button {
                    selectedTab = tab
                } label: {
                    VStack(spacing: 4) {
                        Image(systemName: tab.icon)
                            .font(.title2)
                        Text(tab.title)
                            .font(.caption)
                    }
                    .foregroundStyle(selectedTab == tab ? .blue : .gray)
                    .frame(maxWidth: .infinity)
                }
            }
        }
        .padding(.vertical, 8)
        .background(.bar)
    }
}

// Usage
struct RootView: View {
    @State private var selectedTab: AppTab = .home

    var body: some View {
        VStack(spacing: 0) {
            Group {
                switch selectedTab {
                case .home: NavigationStack { HomeView() }
                case .library: NavigationStack { LibraryView() }
                case .profile: NavigationStack { ProfileView() }
                }
            }
            .frame(maxHeight: .infinity)

            CustomTabBar(selectedTab: $selectedTab)
        }
    }
}
```

### Watch Out

- Custom tab bars do not get the system safe area handling for free. You need to account for the home indicator on modern iPhones.
- You lose automatic state preservation that `TabView` provides. Each `switch` case re-creates the view. Use `@State` or a view model to preserve state across tab switches.

---

## Practical Tips

1. **Use semantic placements** (`.primaryAction`, `.cancellationAction`) over positional ones (`.topBarTrailing`). Semantic placements adapt correctly across platforms.

2. **Keyboard toolbar is essential** for number pads. Users cannot dismiss a `.decimalPad` or `.numberPad` keyboard without a Done button.

3. **Hide the tab bar in detail views** with `.toolbar(.hidden, for: .tabBar)` for immersive content like photo viewers or media players.

4. **Keep toolbar items minimal.** Two to three items max per placement. Overloaded toolbars confuse users and look cramped on smaller devices.

5. **Test on both iPhone and iPad.** Toolbar items can shift positions dramatically between compact and regular size classes. What looks right on one screen may be wrong on another.

6. **18pt minimum** applies to toolbar labels too. If you use custom toolbar views with text, keep them readable.
