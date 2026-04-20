# Chapter 06: Controls — Buttons, Toggles, and Pickers

## Button

### Basic Button

```swift
Button("Save") {
    saveDocument()
}

Button(action: saveDocument) {
    Label("Save", systemImage: "square.and.arrow.down")
}
```

### Button Roles

```swift
Button("Delete", role: .destructive) {
    deleteItem()
}

Button("Cancel", role: .cancel) {
    dismiss()
}
```

`.destructive` renders in red. `.cancel` tells the system this dismisses without action (used in dialogs and confirmations).

### Button with Custom Label

```swift
Button {
    startDownload()
} label: {
    HStack {
        Image(systemName: "arrow.down.circle.fill")
            .font(.title2)
        VStack(alignment: .leading) {
            Text("Download").font(.headline)
            Text("42 MB").font(.caption).foregroundStyle(.secondary)
        }
    }
    .padding()
    .background(.blue.opacity(0.1), in: RoundedRectangle(cornerRadius: 12))
}
```

---

## Built-in Button Styles

```swift
Button("Bordered") { }
    .buttonStyle(.bordered)

Button("Bordered Prominent") { }
    .buttonStyle(.borderedProminent)

Button("Borderless") { }
    .buttonStyle(.borderless)

Button("Plain") { }
    .buttonStyle(.plain)
```

| Style | Look |
|-------|------|
| `.automatic` | Platform default |
| `.bordered` | Tinted background, rounded shape |
| `.borderedProminent` | Filled with tint color, white text |
| `.borderless` | Text only, no background |
| `.plain` | No styling at all — just the label |

### Tint Control

```swift
Button("Accept") { }
    .buttonStyle(.borderedProminent)
    .tint(.green)
```

---

## Custom ButtonStyle

Implement the `ButtonStyle` protocol for a reusable button appearance.

```swift
struct ScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .opacity(configuration.isPressed ? 0.8 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

// Usage
Button("Tap Me") { }
    .buttonStyle(ScaleButtonStyle())
```

### PrimitiveButtonStyle

For full control over when the action fires (e.g., requiring a long press).

```swift
struct LongPressButtonStyle: PrimitiveButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .onLongPressGesture {
                configuration.trigger()
            }
    }
}
```

### Watch Out

- `ButtonStyle` gives you `isPressed` state but the system handles the tap. `PrimitiveButtonStyle` gives you full control but you must call `configuration.trigger()` yourself.
- `buttonStyle` applies to all buttons in the subtree. Set it on a container to style every button inside it at once.

---

## Toggle

### Basic Toggle

```swift
@State private var isEnabled = false

Toggle("Notifications", isOn: $isEnabled)

Toggle(isOn: $isEnabled) {
    Label("Notifications", systemImage: "bell")
}
```

### Toggle Styles

```swift
Toggle("Option", isOn: $value)
    .toggleStyle(.switch)      // the default iOS switch

Toggle("Option", isOn: $value)
    .toggleStyle(.button)      // renders as a pressable button

Toggle("Option", isOn: $value)
    .toggleStyle(.checkbox)    // macOS only
```

### Tint

```swift
Toggle("Dark Mode", isOn: $darkMode)
    .tint(.purple)
```

### Watch Out

- `.toggleStyle(.checkbox)` is macOS only. On iOS it falls back to a switch.
- Toggles in a `List` automatically get trailing alignment. Outside a List, they default to leading label with trailing switch.

---

## Picker

### Menu Picker (Default on iOS)

```swift
@State private var selectedFlavor = "Chocolate"
let flavors = ["Chocolate", "Vanilla", "Strawberry"]

Picker("Flavor", selection: $selectedFlavor) {
    ForEach(flavors, id: \.self) { flavor in
        Text(flavor)
    }
}
```

### Segmented

```swift
Picker("View", selection: $viewMode) {
    Text("Grid").tag(ViewMode.grid)
    Text("List").tag(ViewMode.list)
    Text("Gallery").tag(ViewMode.gallery)
}
.pickerStyle(.segmented)
```

### Wheel

```swift
Picker("Weight", selection: $weight) {
    ForEach(100...300, id: \.self) { w in
        Text("\(w) lbs").tag(w)
    }
}
.pickerStyle(.wheel)
```

### Inline (Expands in List)

```swift
Picker("Category", selection: $selectedCategory) {
    ForEach(categories) { cat in
        Text(cat.name).tag(cat)
    }
}
.pickerStyle(.inline)
```

### Navigation Link Picker

Inside a `NavigationStack`, this pushes a full selection list.

```swift
Picker("Country", selection: $selectedCountry) {
    ForEach(countries) { country in
        Text(country.name).tag(country)
    }
}
.pickerStyle(.navigationLink)
```

### Watch Out — The #1 Picker Bug

Every picker option must have a `.tag()` that matches the **exact type** of the `selection` binding. If your selection is `Optional<Item>`, your tags must be `Optional<Item>` too — not plain `Item`.

```swift
// WRONG — selection is Item?, but tags are Item
@State private var selected: Item?
Picker("Pick", selection: $selected) {
    Text("None").tag(nil)          // nil has no type context
    ForEach(items) { item in
        Text(item.name).tag(item)  // Item, not Item?
    }
}

// RIGHT
Picker("Pick", selection: $selected) {
    Text("None").tag(nil as Item?)
    ForEach(items) { item in
        Text(item.name).tag(item as Item?)
    }
}
```

This is the number one source of "my picker doesn't update" bugs. If the picker does not respond to taps, check tag types first.

---

## Stepper

```swift
@State private var quantity = 1

Stepper("Quantity: \(quantity)", value: $quantity, in: 1...99)

Stepper(value: $zoomLevel, in: 0.5...3.0, step: 0.25) {
    Text("Zoom: \(zoomLevel, specifier: "%.2f")x")
}
```

### Manual Stepper

```swift
Stepper("Custom") {
    increment()
} onDecrement: {
    decrement()
}
```

---

## Slider

```swift
@State private var volume: Double = 0.5

Slider(value: $volume)

Slider(value: $volume, in: 0...100, step: 5) {
    Text("Volume")
} minimumValueLabel: {
    Image(systemName: "speaker")
} maximumValueLabel: {
    Image(systemName: "speaker.wave.3")
}
```

### Watch Out

- Slider labels are hidden by default in many contexts. Use an explicit `Text` above the slider if you need the user to see the label.
- `step` only snaps during dragging. Setting `step: 5` with range `0...100` means the user drags in increments of 5.

---

## DatePicker

```swift
@State private var date = Date()

DatePicker("Birthday", selection: $date, displayedComponents: .date)

DatePicker("Alarm", selection: $date, displayedComponents: .hourAndMinute)

DatePicker("Event", selection: $date,
           in: Date()...,   // only future dates
           displayedComponents: [.date, .hourAndMinute])
```

### Styles

```swift
.datePickerStyle(.graphical)    // calendar grid
.datePickerStyle(.wheel)        // spinning wheels
.datePickerStyle(.compact)      // tappable pill that expands
.datePickerStyle(.automatic)    // platform decides
```

### Watch Out

- `.graphical` takes up a lot of space. Works well in a Form or sheet, but can break layouts in tight spaces.
- The `in:` parameter sets the selectable range. `Date()...` means today onward. `...Date()` means up to today.

---

## ColorPicker

```swift
@State private var color: Color = .blue

ColorPicker("Theme Color", selection: $color)

ColorPicker("Background", selection: $color, supportsOpacity: false)
```

`supportsOpacity: false` hides the alpha slider.

---

## Disabled States

```swift
Button("Submit") { submit() }
    .disabled(formIsInvalid)

Toggle("Feature", isOn: $feature)
    .disabled(!isPremiumUser)
```

`.disabled(true)` grays out the control and blocks interaction. It propagates down the view tree — disable a `VStack` and every control inside is disabled.

### Reading Disabled State in Custom Views

```swift
struct MyControl: View {
    @Environment(\.isEnabled) var isEnabled

    var body: some View {
        Text("Status: \(isEnabled ? "Active" : "Disabled")")
            .foregroundStyle(isEnabled ? .primary : .secondary)
    }
}
```

---

## Labels and Accessibility

### Label

`Label` pairs an icon with text. Many controls accept a `Label` as content.

```swift
Label("Downloads", systemImage: "arrow.down.circle")
Label("Warning", systemImage: "exclamationmark.triangle")
    .foregroundStyle(.orange)
```

### Label Styles

```swift
Label("Item", systemImage: "star")
    .labelStyle(.titleAndIcon)  // both text and icon
    .labelStyle(.titleOnly)     // text only
    .labelStyle(.iconOnly)      // icon only
```

### Accessibility Labels

```swift
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")

Slider(value: $brightness)
    .accessibilityLabel("Screen brightness")
    .accessibilityValue("\(Int(brightness))%")
```

### Watch Out

- Icon-only buttons must have an `.accessibilityLabel`. VoiceOver users hear nothing otherwise.
- `Label` does not always show both icon and text. In toolbars and menus, the system may choose to show only one. Use `.labelStyle(.titleAndIcon)` to force both.

---

## Practical Tips

1. **Use `.borderedProminent` sparingly.** One prominent button per screen for the primary action. Everything else gets `.bordered` or `.borderless`.

2. **Picker tag type matching** is the most common SwiftUI bug. When your picker ignores taps, check tag types first.

3. **Stepper is great for small ranges** (1-20). For large ranges, use a Slider or a text field with validation.

4. **Group related controls in a `Form`.** Controls inside a Form automatically get platform-appropriate styling — grouped rows on iOS, aligned labels on macOS.

5. **Test with Dynamic Type.** At the largest accessibility sizes, labels wrap and controls reflow. Make sure nothing gets clipped.

6. **18pt minimum font height.** Per project standards, all text in controls should meet this minimum for iPad readability.
