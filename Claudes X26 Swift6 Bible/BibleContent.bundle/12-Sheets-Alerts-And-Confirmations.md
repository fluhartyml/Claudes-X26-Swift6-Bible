# Chapter 12: Sheets, Alerts, and Confirmations

## Live Reference: Claudes LockBox

> **Claudes LockBox** ships every pattern in this chapter at production scale. The New Item form lives in a `fullScreenCover` (not a `.sheet` — see Build-Along 03 §10 for why the `.sheet` height fights the iOS keyboard on phone-sized screens). The image viewer opens via `.sheet`. Long-press menus on photos use the SwiftUI contextual-menu pattern. Delete operations use confirmation dialogs. The About sheet opens from the sidebar's info button via `.sheet` again. Source: [github.com/fluhartyml/Claudes-LockBox](https://github.com/fluhartyml/Claudes-LockBox). See Build-Along 03 for the full walkthrough; the `fullScreenCover` vs `.sheet` decision is one of three polish fixes from a single commit on the build day, captured in Section 10 of that chapter.

---

## X26 Updates to Sheets and Action Sheets

Modal views in X26 adopt Liquid Glass and a refreshed shape. Sheets gain an increased corner radius. **Half sheets are inset from the edge of the display** so content peeks through from underneath; when a half sheet expands to full height, it transitions to a more opaque appearance to keep focus on the task[^s1].

Two practical review tasks:

- **Inside the sheet:** check content and controls near the rounder corners. Anything that was tight against a sharp pre-X26 corner can clip or look cramped against the X26 corner radius.
- **Outside the sheet:** for half sheets, check what shows through the inset gap between the sheet and the display edge. The peek-through is intentional, but a busy or high-contrast background can fight the sheet for attention.

If you've added a custom visual effect view as a sheet or popover background, remove it. Apple's guidance is explicit: *"Audit the backgrounds of sheets and popovers... remove those custom background views to provide a consistent experience with other sheets across the system."*

### Action Sheets Originate from Their Source

Action sheets in X26 don't slide up from the bottom edge of the display anymore. They originate from the element that triggered them — and they stay non-modal, so the user can interact with the rest of the interface while the sheet is open. The relevant SwiftUI API:

```swift
.confirmationDialog(
    "Delete this item?",
    isPresented: $showDeletePrompt,
    titleVisibility: .visible,
    presenting: itemToDelete
) { item in
    Button("Delete", role: .destructive) {
        delete(item)
    }
    Button("Cancel", role: .cancel) {}
}
```

Set the source view or item via the sheet's anchor configuration so the system knows where to originate the inline appearance from. Without an anchor, the dialog falls back to the older bottom-edge behavior.

[^s1]: Apple Developer Documentation, *Adopting Liquid Glass*. <https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass> — verified 2026-04-29.

---

## Sheets

### Basic Sheet

Present a modal sheet with a boolean binding:

```swift
@State private var showSettings = false

Button("Settings") { showSettings = true }
    .sheet(isPresented: $showSettings) {
        SettingsView()
    }
```

The sheet dismisses automatically when `showSettings` becomes `false`.

### Sheet with an Item

Present a sheet driven by an optional identifiable value:

```swift
@State private var selectedProject: Project?

List(projects) { project in
    Button(project.name) {
        selectedProject = project
    }
}
.sheet(item: $selectedProject) { project in
    ProjectDetailView(project: project)
}
```

The sheet appears when the value is non-nil and dismisses when it becomes `nil`. This is the preferred pattern when the sheet content depends on which item was tapped.

**Watch out:** The item type must conform to `Identifiable`. If it doesn't, add conformance or use the boolean variant.

### Dismissing a Sheet from Inside

Use the `dismiss` environment value:

```swift
struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form { /* ... */ }
                .toolbar {
                    Button("Done") { dismiss() }
                }
        }
    }
}
```

**Watch out:** Always wrap sheet content in a `NavigationStack` if you want a toolbar with Done/Cancel buttons. Without it, `.toolbar` has nowhere to render.

### Preventing Dismissal

Stop the user from swiping down to dismiss:

```swift
.sheet(isPresented: $showEditor) {
    EditorView()
        .interactiveDismissDisabled(hasUnsavedChanges)
}
```

Pass a boolean to conditionally prevent dismissal. When `true`, the swipe-down gesture is disabled and the user must use your explicit dismiss button.

### onDismiss Callback

Run code when the sheet closes:

```swift
.sheet(isPresented: $showPicker, onDismiss: {
    refreshData()
}) {
    PhotoPicker()
}
```

---

## Sheet Detents

Control how tall a sheet is on iPhone/iPad.

### Built-in Detents

```swift
.sheet(isPresented: $showInfo) {
    InfoView()
        .presentationDetents([.medium, .large])
}
```

- `.medium` -- half screen
- `.large` -- full height (default)

The user can drag between the detents you provide.

### Fixed and Fractional Detents

```swift
.presentationDetents([
    .height(200),          // fixed 200pt
    .fraction(0.3),        // 30% of screen
    .medium,
    .large
])
```

### Custom Detents

For dynamic sizing:

```swift
struct CompactDetent: CustomPresentationDetent {
    static func height(in context: Context) -> CGFloat? {
        min(context.maxDetentValue, 400)
    }
}

// Usage
.presentationDetents([.custom(CompactDetent.self), .large])
```

### Detent Selection Binding

Track and control which detent is active:

```swift
@State private var selectedDetent: PresentationDetent = .medium

.sheet(isPresented: $showPanel) {
    PanelView()
        .presentationDetents([.medium, .large], selection: $selectedDetent)
}
```

### Drag Indicator

```swift
.presentationDragIndicator(.visible)   // show the grabber bar
.presentationDragIndicator(.hidden)    // hide it
```

### Background Interaction

Allow the user to interact with content behind the sheet:

```swift
.presentationBackgroundInteraction(.enabled(upThrough: .medium))
```

This lets taps pass through to the parent view when the sheet is at `.medium` or smaller.

### Sheet Background and Corner Radius

```swift
.presentationBackground(.ultraThinMaterial)
.presentationCornerRadius(20)
```

---

## fullScreenCover

A modal that covers the entire screen. No swipe-to-dismiss gesture.

```swift
@State private var showOnboarding = false

.fullScreenCover(isPresented: $showOnboarding) {
    OnboardingView()
}
```

Works identically to `.sheet` in terms of API (boolean binding, item binding, `onDismiss`).

**Watch out:** `fullScreenCover` has no swipe-to-dismiss. You must provide your own dismiss button. If you forget, the user is stuck.

```swift
struct OnboardingView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack {
            // onboarding content
            Button("Get Started") { dismiss() }
        }
    }
}
```

`fullScreenCover` does not support detents. It is always full screen.

---

## Popover

A floating bubble anchored to the source view. On iPad and Mac it appears as an actual popover. On iPhone it falls back to a sheet.

```swift
@State private var showTooltip = false

Button("Info") { showTooltip = true }
    .popover(isPresented: $showTooltip) {
        Text("This is additional information about the feature.")
            .font(.body)
            .padding()
    }
```

### Popover with Arrow Edge

```swift
.popover(isPresented: $showPopover, arrowEdge: .top) {
    PopoverContent()
}
```

Arrow edge options: `.top`, `.bottom`, `.leading`, `.trailing`. The system may override this if there is not enough space.

### Sizing a Popover

On iPad/Mac, constrain the popover size:

```swift
.popover(isPresented: $showPopover) {
    PopoverContent()
        .frame(width: 300, height: 400)
}
```

**Watch out:** On iPhone, popovers become sheets. Do not rely on popover-specific behavior for iPhone layouts.

---

## Alerts

### Basic Alert

```swift
@State private var showAlert = false

Button("Delete") { showAlert = true }
    .alert("Delete Item?", isPresented: $showAlert) {
        Button("Delete", role: .destructive) { deleteItem() }
        Button("Cancel", role: .cancel) { }
    } message: {
        Text("This action cannot be undone.")
    }
```

### Alert with No Message

```swift
.alert("Are you sure?", isPresented: $showAlert) {
    Button("Yes") { proceed() }
    Button("No", role: .cancel) { }
}
```

If you omit the `message:` parameter, the alert shows only the title and buttons.

### Alert with an Item

```swift
@State private var errorToShow: AppError?

.alert("Error", isPresented: Binding(
    get: { errorToShow != nil },
    set: { if !$0 { errorToShow = nil } }
)) {
    Button("OK") { errorToShow = nil }
} message: {
    Text(errorToShow?.localizedDescription ?? "")
}
```

Or more cleanly, make your error type `Identifiable` and use the item variant:

```swift
struct AppError: Identifiable {
    let id = UUID()
    let message: String
}

@State private var currentError: AppError?

.alert(item: $currentError) { error in
    // This closure does not exist in the standard API.
    // Use the pattern below instead.
}
```

**Practical pattern** -- the cleanest alert-with-item approach:

```swift
@State private var alertMessage = ""
@State private var showErrorAlert = false

func handleError(_ error: Error) {
    alertMessage = error.localizedDescription
    showErrorAlert = true
}

.alert("Error", isPresented: $showErrorAlert) {
    Button("OK", role: .cancel) { }
} message: {
    Text(alertMessage)
}
```

### Alert with TextField

Alerts can contain text fields:

```swift
@State private var showRename = false
@State private var newName = ""

.alert("Rename", isPresented: $showRename) {
    TextField("New name", text: $newName)
    Button("Rename") { rename(to: newName) }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("Enter a new name for this item.")
}
```

**Watch out:** Alert text fields are iOS 16+ / macOS 13+.

### Button Roles

- `.destructive` -- red text, signals danger
- `.cancel` -- bold text, always placed in the "safe" position

```swift
.alert("Reset?", isPresented: $showReset) {
    Button("Reset Everything", role: .destructive) { reset() }
    Button("Cancel", role: .cancel) { }
}
```

If you provide no `.cancel` button, the system adds one automatically.

---

## Confirmation Dialog

An action sheet on iPhone, a popover menu on iPad/Mac. Use for choices where the user picks from options.

```swift
@State private var showDialog = false

Button("Share") { showDialog = true }
    .confirmationDialog("Share As", isPresented: $showDialog, titleVisibility: .visible) {
        Button("PDF") { shareAsPDF() }
        Button("Image") { shareAsImage() }
        Button("Text") { shareAsText() }
        Button("Cancel", role: .cancel) { }
    } message: {
        Text("Choose the export format.")
    }
```

### Title Visibility

```swift
.confirmationDialog("Title", isPresented: $show, titleVisibility: .visible) { }
.confirmationDialog("Title", isPresented: $show, titleVisibility: .hidden) { }
.confirmationDialog("Title", isPresented: $show, titleVisibility: .automatic) { }
```

On iPhone, `.automatic` hides the title. Set `.visible` if you want users to see it.

### Confirmation Dialog with Item

```swift
@State private var itemToDelete: Item?

.confirmationDialog("Delete", isPresented: Binding(
    get: { itemToDelete != nil },
    set: { if !$0 { itemToDelete = nil } }
), titleVisibility: .visible) {
    if let item = itemToDelete {
        Button("Delete \(item.name)", role: .destructive) {
            delete(item)
            itemToDelete = nil
        }
    }
    Button("Cancel", role: .cancel) { itemToDelete = nil }
} message: {
    Text("This will permanently remove the item.")
}
```

---

## Inspector

The `.inspector` modifier presents a side panel on iPad/Mac and a sheet on iPhone. Ideal for detail/property panels.

```swift
@State private var showInspector = false

NavigationStack {
    ContentView()
        .toolbar {
            Button("Inspector", systemImage: "info.circle") {
                showInspector.toggle()
            }
        }
        .inspector(isPresented: $showInspector) {
            InspectorContent()
                .inspectorColumnWidth(min: 200, ideal: 300, max: 400)
        }
}
```

### Inspector Column Width

```swift
.inspectorColumnWidth(300)                          // fixed width
.inspectorColumnWidth(min: 200, ideal: 300, max: 400)  // flexible range
```

**Watch out:** `.inspector` was introduced in iOS 17 / macOS 14. On older systems, you need a different approach (NavigationSplitView sidebar, etc.).

---

## Presentation Order and Stacking

### Multiple Sheets

You cannot attach two `.sheet` modifiers to the same view. Each view gets one `.sheet`, one `.fullScreenCover`, one `.alert`, etc.

```swift
// WRONG -- only one of these will work
Button("Tap")
    .sheet(isPresented: $showA) { ViewA() }
    .sheet(isPresented: $showB) { ViewB() }

// RIGHT -- attach to different views
VStack {
    Button("Show A") { showA = true }
        .sheet(isPresented: $showA) { ViewA() }

    Button("Show B") { showB = true }
        .sheet(isPresented: $showB) { ViewB() }
}
```

Or use an enum to drive a single sheet:

```swift
enum ActiveSheet: Identifiable {
    case settings, profile, editor

    var id: Self { self }
}

@State private var activeSheet: ActiveSheet?

.sheet(item: $activeSheet) { sheet in
    switch sheet {
    case .settings: SettingsView()
    case .profile: ProfileView()
    case .editor: EditorView()
    }
}
```

This is the cleanest pattern for views that can present multiple different sheets.

### Sheet Over Sheet

You can present a sheet from inside a sheet. The new sheet appears on top:

```swift
struct FirstSheet: View {
    @State private var showSecond = false

    var body: some View {
        Button("Show Second") { showSecond = true }
            .sheet(isPresented: $showSecond) {
                SecondSheet()
            }
    }
}
```

**Watch out:** Deep sheet stacking gets confusing for users. Limit to two levels at most.

---

## Practical Patterns

### Destructive Action Confirmation

```swift
struct DeleteButton: View {
    let itemName: String
    let onDelete: () -> Void
    @State private var showConfirm = false

    var body: some View {
        Button("Delete", role: .destructive) {
            showConfirm = true
        }
        .confirmationDialog("Delete \(itemName)?",
                            isPresented: $showConfirm,
                            titleVisibility: .visible) {
            Button("Delete", role: .destructive) { onDelete() }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This cannot be undone.")
        }
    }
}
```

### Error Alert Modifier

A reusable pattern for showing errors:

```swift
struct ErrorAlert: ViewModifier {
    @Binding var error: Error?

    var isPresented: Binding<Bool> {
        Binding(
            get: { error != nil },
            set: { if !$0 { error = nil } }
        )
    }

    func body(content: Content) -> some View {
        content.alert("Error", isPresented: isPresented) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(error?.localizedDescription ?? "An unknown error occurred.")
        }
    }
}

extension View {
    func errorAlert(_ error: Binding<Error?>) -> some View {
        modifier(ErrorAlert(error: error))
    }
}

// Usage
@State private var lastError: Error?

SomeView()
    .errorAlert($lastError)
```

### Half-Sheet Settings Panel

```swift
@State private var showSettings = false

.sheet(isPresented: $showSettings) {
    NavigationStack {
        SettingsForm()
            .navigationTitle("Settings")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { showSettings = false }
                }
            }
    }
    .presentationDetents([.medium, .large])
    .presentationDragIndicator(.visible)
    .presentationBackground(.regularMaterial)
}
```

---

## Quick Reference

| What | How |
|---|---|
| Sheet (boolean) | `.sheet(isPresented: $bool) { }` |
| Sheet (item) | `.sheet(item: $optional) { item in }` |
| Full screen modal | `.fullScreenCover(isPresented: $bool) { }` |
| Popover | `.popover(isPresented: $bool) { }` |
| Alert | `.alert("Title", isPresented: $bool) { buttons } message: { }` |
| Confirmation dialog | `.confirmationDialog("Title", isPresented: $bool) { buttons }` |
| Inspector panel | `.inspector(isPresented: $bool) { }` |
| Dismiss from inside | `@Environment(\.dismiss) private var dismiss` |
| Block swipe dismiss | `.interactiveDismissDisabled(true)` |
| Half sheet | `.presentationDetents([.medium, .large])` |
| Custom height | `.presentationDetents([.height(300)])` |
| Drag indicator | `.presentationDragIndicator(.visible)` |
| Sheet background | `.presentationBackground(.thinMaterial)` |
| Background interaction | `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` |
| Inspector width | `.inspectorColumnWidth(min: 200, ideal: 300, max: 400)` |
