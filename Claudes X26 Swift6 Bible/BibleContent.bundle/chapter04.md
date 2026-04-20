# Chapter 4: Gestures and Input

*Claude's Xcode 26 Swift Bible — Part II: The User Interface*

---

## 1. How Users Interact With Your App

1.1 Every Apple platform has a different way of receiving input from the user. iPhones and iPads use touch. Macs use a mouse, trackpad, and keyboard. Apple TVs use the Siri Remote and a focus system — no touching the screen. Apple Watch uses taps, the Digital Crown, and the side button. Vision Pro uses eye tracking and hand gestures. Your app needs to handle whatever input the platform gives it.

1.2 SwiftUI abstracts most of this for you. A `Button` works on every platform — it responds to a tap on iPhone, a click on Mac, a select on Apple TV, and a gaze-and-tap on Vision Pro. You write it once and SwiftUI translates the input method. But when you need more control — detecting swipes, long presses, drags, pinches, or rotations — you use **gestures**.

---

## 2. Tap Gesture [all]

2.1 The simplest gesture. The user taps (or clicks) something and your code runs.

```swift
Text("Tap me")
    .font(.system(size: 18))
    .onTapGesture {
        print("Tapped!")
    }
```

2.2 You can require multiple taps:

```swift
Text("Double-tap me")
    .font(.system(size: 18))
    .onTapGesture(count: 2) {
        print("Double tapped!")
    }
```

2.3 **When to use a tap gesture vs a Button:** Use a `Button` when there's an obvious action — "Save," "Delete," "Play." Use `.onTapGesture` when you're making a non-button element interactive — tapping an image to expand it, tapping a row to select it. Buttons give you built-in accessibility, focus support, and visual feedback. Tap gestures give you none of that unless you add it yourself.

---

## 3. Long Press Gesture [iOS] [macOS]

3.1 The user presses and holds. Common for context menus, entering edit mode, or "hold to confirm" destructive actions.

```swift
Text("Hold me")
    .font(.system(size: 18))
    .onLongPressGesture(minimumDuration: 0.5) {
        print("Long pressed!")
    }
```

3.2 You can show feedback while the user is holding by using `@GestureState`:

```swift
struct HoldButton: View {
    @GestureState private var isHolding = false

    var body: some View {
        Circle()
            .fill(isHolding ? .green : .gray)
            .frame(width: 80, height: 80)
            .gesture(
                LongPressGesture(minimumDuration: 1.0)
                    .updating($isHolding) { value, state, _ in
                        state = value
                    }
                    .onEnded { _ in
                        print("Confirmed!")
                    }
            )
    }
}
```

3.3 `@GestureState` automatically resets to its initial value when the gesture ends or is cancelled. You don't have to clean it up.

---

## 4. Drag Gesture [iOS] [macOS] [visionOS]

4.1 The user presses and moves their finger (or mouse) across the screen. Useful for sliders, movable elements, or swipe-to-dismiss.

```swift
struct DraggableBox: View {
    @State private var offset = CGSize.zero

    var body: some View {
        RoundedRectangle(cornerRadius: 12)
            .fill(.blue)
            .frame(width: 100, height: 100)
            .offset(offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                    }
                    .onEnded { _ in
                        offset = .zero  // snap back
                    }
            )
    }
}
```

4.2 The `value` in `.onChanged` gives you:
- `.translation` — how far the finger has moved from the start point
- `.location` — where the finger is right now
- `.startLocation` — where the finger first touched
- `.predictedEndLocation` — where SwiftUI thinks the finger is heading (useful for flick-to-dismiss)

---

## 5. Magnify Gesture (Pinch to Zoom) [iOS] [macOS] [visionOS]

5.1 Two fingers moving apart or together. The classic pinch-to-zoom.

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Image("photo")
            .resizable()
            .scaledToFit()
            .scaleEffect(scale)
            .gesture(
                MagnifyGesture()
                    .onChanged { value in
                        scale = value.magnification
                    }
                    .onEnded { _ in
                        scale = max(scale, 1.0)  // don't go smaller than original
                    }
            )
    }
}
```

5.2 On macOS, this works with a trackpad pinch or Ctrl+scroll.

---

## 6. Rotate Gesture [iOS] [macOS] [visionOS]

6.1 Two fingers twisting. Used for rotating images, dials, or knobs.

```swift
struct RotatableView: View {
    @State private var angle: Angle = .zero

    var body: some View {
        Image(systemName: "arrow.up")
            .font(.system(size: 48))
            .rotationEffect(angle)
            .gesture(
                RotateGesture()
                    .onChanged { value in
                        angle = value.rotation
                    }
            )
    }
}
```

---

## 7. Combining Gestures [all]

7.1 Sometimes you need more than one gesture on the same view. SwiftUI gives you three ways to combine them:

7.2 **Simultaneous** — both gestures run at the same time. Good for pinch-and-rotate together.

```swift
.gesture(
    MagnifyGesture()
        .simultaneously(with: RotateGesture())
)
```

7.3 **Sequenced** — one gesture must complete before the next one starts. Good for "long press then drag."

```swift
.gesture(
    LongPressGesture()
        .sequenced(before: DragGesture())
)
```

7.4 **Exclusive** — only one gesture wins. The first one to be recognized takes over. Good for "tap or long press, not both."

```swift
.gesture(
    TapGesture()
        .exclusively(before: LongPressGesture())
)
```

7.5 **Priority.** If a child view and a parent view both have gestures, the child wins by default. To let the parent take priority:

```swift
.highPriorityGesture(TapGesture().onEnded { ... })
```

To let both run:

```swift
.simultaneousGesture(TapGesture().onEnded { ... })
```

---

## 8. The tvOS Focus System [tvOS]

8.1 Apple TV has no touchscreen. Users navigate with the Siri Remote — swiping to move focus between elements and pressing to select. SwiftUI handles focus automatically for standard controls (buttons, lists, toggles), but you need to understand how it works.

8.2 **Focus 101:** One element on screen is "focused" at a time — it's highlighted and ready to receive input. Swiping the remote moves focus to the next element in that direction. Pressing the remote's center button triggers the focused element.

8.3 **@FocusState** lets you track and control which element has focus:

```swift
struct TVMenu: View {
    @FocusState private var focusedItem: String?

    var body: some View {
        VStack(spacing: 20) {
            Button("Play") { }
                .focused($focusedItem, equals: "play")
            Button("Settings") { }
                .focused($focusedItem, equals: "settings")
        }
        .font(.system(size: 28))
        .onAppear {
            focusedItem = "play"  // start focus on Play
        }
    }
}
```

8.4 **Watch out:** On tvOS, if nothing is focusable on screen, the user is stuck — they can't interact with anything. Always make sure at least one element is focusable. The Siri Remote's arrow keys map to swipe directions in the simulator. The tvOS focus highlight is system-managed — don't fight it with custom highlights unless you know what you're doing.

_8.5 **Numbering your focus map.** If spatial focus isn't behaving the way you expect — focus skipping elements, landing in the wrong place, or highlights not showing — try mapping every interactive element to a numbered enum. This gives you a wiring diagram of your remote navigation:

```swift
enum FocusItem: Int, CaseIterable {
    case shuffle = 1
    case repeatOne = 2
    case repeatAll = 3
    case timer = 4
    case station1 = 5
    // ...every interactive element gets a number
}

@FocusState private var focused: FocusItem?
```

With this map, you can force focus to any element by setting `focused = .shuffle`, and you can debug focus issues by printing which number is currently focused. It's also a fallback — if SwiftUI's automatic spatial navigation can't figure out your layout, you can manually control the order with `.onMoveCommand` and increment/decrement the number. Most of the time you won't need this, but when focus breaks, having the numbered map saves hours of guessing. Speaking from experience — a tvOS focus issue once cost an entire day of debugging, led to a full rollback, and was only resolved the next day with a clean rebuild. The numbered map didn't exist yet. It does now.

---

## 9. macOS Keyboard Shortcuts [macOS]

9.1 On Mac, users expect keyboard shortcuts for common actions. SwiftUI makes this easy:

```swift
Button("Save") {
    save()
}
.keyboardShortcut("s", modifiers: .command)  // Cmd+S
```

9.2 You can also add shortcuts to menu commands:

```swift
.commands {
    CommandGroup(replacing: .newItem) {
        Button("New Document") {
            createDocument()
        }
        .keyboardShortcut("n", modifiers: .command)
    }
}
```

9.3 **Common shortcut modifiers:**
- `.command` — Cmd key
- `.shift` — Shift key
- `.option` — Option key
- `.control` — Control key

Combine them: `.modifiers([.command, .shift])` for Cmd+Shift.

---

## 10. Accessibility Actions [all]

10.1 Not every user can tap, swipe, or pinch. VoiceOver users navigate with screen reader commands. Your gestures need accessible alternatives.

```swift
Image("photo")
    .accessibilityLabel("Vacation photo")
    .accessibilityAction(.magicTap) {
        toggleFullscreen()
    }
    .accessibilityAction(named: "Zoom In") {
        scale += 0.5
    }
    .accessibilityAction(named: "Zoom Out") {
        scale -= 0.5
    }
```

10.2 **The rule:** If a gesture does something important, add an accessibility action that does the same thing without requiring the gesture. A VoiceOver user can't pinch to zoom — give them a "Zoom In" action instead.

---

## 11. Tips

11.1 **Use Button for most interactions.** Buttons handle accessibility, focus, keyboard shortcuts, and visual feedback for free. Only reach for custom gestures when Button doesn't fit.

11.2 **Keep gestures discoverable.** A hidden long-press or swipe is a feature nobody uses. Pair gestures with visible UI hints — "Hold to delete" text, a drag handle icon, instructions on first launch.

11.3 **Test on real devices.** Gesture timing feels completely different on a real phone vs the simulator. A comfortable long-press duration on a trackpad is too long on a phone.

11.4 **On tvOS, trust the focus system.** Standard SwiftUI controls get focus automatically. Fight it and you'll spend hours debugging highlight behavior. Custom focus only when you truly need it.

11.5 **Gesture state resets automatically with @GestureState.** Use it for temporary visual feedback (scaling up while holding, dimming while dragging). Use @State for changes that should persist after the gesture ends.

---

*Claude's Xcode 26 Swift Bible — Chapter 4*
*By Dr. Wahl — co-authored by Claude A. and Michael Fluharty. Swift 6, Xcode 26.*
