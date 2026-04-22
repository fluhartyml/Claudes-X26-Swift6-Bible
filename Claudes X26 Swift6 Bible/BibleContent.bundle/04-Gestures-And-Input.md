# Chapter 4: Gestures & Input

**Claude's Swift Reference 26** -- Part III: The User Interface

---

## What This Chapter Is About

Books 01 through 03 built up the language, SwiftUI's view model, and the scene/window structure of an Apple app. The app runs; views draw. Now we turn to the other half of an app's life: how the user talks back. Taps, swipes, drags, pinches, keyboard presses, Apple Pencil strokes.

SwiftUI covers this with two layers of API:

- **High-level shortcuts** built into the common views -- `Button`, `TextField`, `Toggle`, `onTapGesture`, `onSubmit`. Most apps live here and go no deeper.
- **The Gesture protocol** -- a composable system for building, combining, and tracking touch gestures when the shortcuts don't cover what you need.

This chapter walks both layers. The goal is that by the end you can handle any ordinary input path a user will hand your app, and know which door to open for the uncommon ones.

---

## The Tap -- The Simplest Input

A tap is a single, quick press-and-release in roughly the same spot. Every tappable element in an Apple app begins with a tap.

### onTapGesture

The shortest form. Attach `.onTapGesture` to any view and hand it a closure.

```swift
Text("Hello")
    .onTapGesture {
        print("tapped")
    }
```

That's it. The view becomes tappable; the closure fires every time.

You can ask for a specific number of taps:

```swift
Text("Double-tap me")
    .onTapGesture(count: 2) {
        print("double-tap")
    }
```

And you can read the tap location on iOS 16 and later:

```swift
GeometryReader { proxy in
    Color.blue
        .onTapGesture { location in
            print("tapped at \(location)")
        }
}
```

The location is in the view's own coordinate space.

### Button vs onTapGesture

`Button` and `.onTapGesture` both handle taps. They are not interchangeable.

Use `Button` when the tap triggers an action the user can describe in words: "Save", "Delete", "Next". The system gets you accessibility, focus behavior on Apple TV, keyboard activation, and the platform-correct pressed state for free.

Use `.onTapGesture` when the tapped thing is a graphic element -- an image card, a color swatch, a shape on a canvas -- where a button's default styling would fight you.

A rough rule: if VoiceOver should read "Button" when it lands on the view, use `Button`. If it should read "Image" or "Graphic", use `.onTapGesture`.

---

## The Long Press

A long press fires after the user holds their finger down for at least 0.5 seconds without moving much.

```swift
Image(systemName: "star")
    .onLongPressGesture {
        print("long-pressed")
    }
```

You can customize how long and how far the finger is allowed to drift:

```swift
Image(systemName: "star")
    .onLongPressGesture(minimumDuration: 1.0, maximumDistance: 10) {
        print("long-pressed")
    }
```

Long-press is the gesture for "I want the extra menu." Context menus, share menus, and drag-to-reorder all start from it. SwiftUI's `.contextMenu` modifier wires the gesture automatically -- you rarely call `onLongPressGesture` yourself when a context menu is what you want.

```swift
Text("Item")
    .contextMenu {
        Button("Rename") { /* ... */ }
        Button("Delete", role: .destructive) { /* ... */ }
    }
```

---

## Drag

A drag gesture reports the finger's position continuously from the first touch until the lift.

### DragGesture

`DragGesture` is a `Gesture` type. You hand it to the `.gesture` modifier and attach closures with `.onChanged` and `.onEnded`:

```swift
struct DragDot: View {
    @State private var offset: CGSize = .zero

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 80, height: 80)
            .offset(offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                    }
                    .onEnded { _ in
                        withAnimation(.spring) { offset = .zero }
                    }
            )
    }
}
```

`value.translation` is a `CGSize` of how far the finger has moved since the gesture started. `value.location` is where the finger currently is. `value.startLocation` is where it first touched down.

The example above moves the dot while dragging and snaps it back on release.

### @GestureState vs @State

If you write the drag example above with `@State` for the offset, you have to clear it yourself in `.onEnded`. Miss a case and the dot sticks. `@GestureState` fixes that.

```swift
struct DragDot: View {
    @GestureState private var drag: CGSize = .zero

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 80, height: 80)
            .offset(drag)
            .gesture(
                DragGesture()
                    .updating($drag) { value, state, _ in
                        state = value.translation
                    }
            )
    }
}
```

`@GestureState` automatically resets to its initial value (`.zero`) as soon as the gesture ends or is cancelled by the system. You never write cleanup code, and you never have a stuck dot.

The rule of thumb: use `@GestureState` for the in-flight position you only care about while dragging, and `@State` for any state you want to persist after the gesture ends (like the dot's final resting spot).

A combined example -- a dot that stays where you drop it:

```swift
struct StickyDot: View {
    @State private var position: CGSize = .zero
    @GestureState private var drag: CGSize = .zero

    var body: some View {
        Circle()
            .fill(.orange)
            .frame(width: 80, height: 80)
            .offset(x: position.width + drag.width,
                    y: position.height + drag.height)
            .gesture(
                DragGesture()
                    .updating($drag) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        position.width  += value.translation.width
                        position.height += value.translation.height
                    }
            )
    }
}
```

The `drag` value feeds the live offset; `position` remembers where the dot settled.

---

## Pinch and Rotate

`MagnifyGesture` and `RotateGesture` work the same way as `DragGesture` -- both are `Gesture` types you attach with `.gesture` and observe with `.onChanged` / `.onEnded` / `.updating`.

```swift
struct Zoomer: View {
    @State private var scale: CGFloat = 1.0
    @GestureState private var livePinch: CGFloat = 1.0

    var body: some View {
        Image(systemName: "photo.artframe")
            .resizable()
            .frame(width: 200, height: 200)
            .scaleEffect(scale * livePinch)
            .gesture(
                MagnifyGesture()
                    .updating($livePinch) { value, state, _ in
                        state = value.magnification
                    }
                    .onEnded { value in
                        scale *= value.magnification
                    }
            )
    }
}
```

`value.magnification` is the ratio between the current two-finger distance and the distance at the gesture's start. It begins at 1.0, grows as fingers spread, shrinks as they pinch.

`RotateGesture` gives you a `value.rotation` as an `Angle`:

```swift
.gesture(
    RotateGesture()
        .onChanged { value in
            rotation = value.rotation
        }
)
```

Pinch and rotate are almost always used together on a photo or map view. SwiftUI lets you combine them.

---

## Combining Gestures

Three composition operators let you describe how two gestures relate:

- `.simultaneously(with:)` -- both gestures track at the same time
- `.sequenced(before:)` -- the second gesture only starts after the first ends
- `.exclusively(before:)` -- exactly one of the two recognizes; the other is dropped

### Simultaneous -- Pinch and Rotate Together

```swift
struct PhotoEditor: View {
    @State private var scale: CGFloat = 1.0
    @State private var rotation: Angle = .zero

    var body: some View {
        Image("kitten")
            .resizable()
            .scaledToFit()
            .scaleEffect(scale)
            .rotationEffect(rotation)
            .gesture(
                MagnifyGesture()
                    .simultaneously(with: RotateGesture())
                    .onChanged { value in
                        if let m = value.first?.magnification { scale = m }
                        if let r = value.second?.rotation    { rotation = r }
                    }
            )
    }
}
```

When you combine gestures with `.simultaneously`, the closure receives a tuple-shaped value with `.first` and `.second`. Each side is optional because either gesture can be absent at any given instant.

### Sequenced -- Long Press Then Drag

A long-press followed by a drag is the native "grab and move" gesture on iOS.

```swift
struct GrabAndMove: View {
    @State private var offset: CGSize = .zero
    @State private var isLifted = false

    var body: some View {
        let press = LongPressGesture(minimumDuration: 0.3)
        let drag  = DragGesture()

        return RoundedRectangle(cornerRadius: 16)
            .fill(isLifted ? .yellow : .blue)
            .frame(width: 120, height: 80)
            .offset(offset)
            .gesture(
                press.sequenced(before: drag)
                    .onChanged { value in
                        switch value {
                        case .first(true):
                            isLifted = true
                        case .second(true, let dragValue?):
                            offset = dragValue.translation
                        default: break
                        }
                    }
                    .onEnded { _ in
                        withAnimation(.spring) { offset = .zero }
                        isLifted = false
                    }
            )
    }
}
```

The sequenced value is itself an enum: `.first(...)` during the long press, `.second(..., dragValue)` during the drag that follows.

### Exclusively -- Pick One

Use `.exclusively(before:)` when two gestures could both match and you want only one to win, in a specific priority.

```swift
let doubleTap = TapGesture(count: 2).onEnded { /* ... */ }
let singleTap = TapGesture(count: 1).onEnded { /* ... */ }

Text("Tap me")
    .gesture(doubleTap.exclusively(before: singleTap))
```

Without `.exclusively`, a single-tap would fire inside every double-tap.

---

## Focus and the Keyboard

SwiftUI's text inputs (`TextField`, `SecureField`, `TextEditor`) handle keystrokes for you. What you usually need to manage is:

1. Which field has the keyboard right now?
2. What happens when the user presses Return or Tab?
3. What keys should trigger app-level actions, regardless of which field is active?

### @FocusState -- Who Has the Keyboard

`@FocusState` binds a property to "which field is focused." You read it to tell which field is active; you write it to move focus programmatically.

```swift
struct LoginForm: View {
    enum Field: Hashable { case username, password }

    @State private var username = ""
    @State private var password = ""
    @FocusState private var focus: Field?

    var body: some View {
        VStack {
            TextField("User", text: $username)
                .focused($focus, equals: .username)
                .submitLabel(.next)
                .onSubmit { focus = .password }

            SecureField("Password", text: $password)
                .focused($focus, equals: .password)
                .submitLabel(.go)
                .onSubmit { /* sign in */ }

            Button("Sign In") { /* sign in */ }
        }
        .padding()
        .onAppear { focus = .username }
    }
}
```

`@FocusState` can be `Bool` (for a single-field form) or any `Hashable` enum (for multiple fields). Each `TextField` calls `.focused($focus, equals: someCase)` to claim its identity.

`.submitLabel(.next)` sets the return key's label. `.onSubmit` fires when the user presses return.

### Keyboard Shortcuts

For Mac apps and iPad apps connected to a hardware keyboard, `.keyboardShortcut` makes a `Button` respond to a key combo:

```swift
Button("Save") { save() }
    .keyboardShortcut("s", modifiers: .command)

Button("Close") { close() }
    .keyboardShortcut(.cancelAction) // Escape
```

The second form uses a role instead of a specific key, so the system picks the right key for the current platform.

Shortcuts defined on buttons in a `Menu` appear as badges in the menu, just like a native app.

### onKeyPress -- Raw Keys

When you need to respond to individual keys outside of a text field -- arrow keys in a game, space bar for play/pause -- use `.onKeyPress`:

```swift
struct CursorBox: View {
    @State private var position: CGPoint = .init(x: 100, y: 100)

    var body: some View {
        Circle()
            .fill(.red)
            .frame(width: 30, height: 30)
            .position(position)
            .focusable()
            .onKeyPress(.leftArrow)  { position.x -= 10; return .handled }
            .onKeyPress(.rightArrow) { position.x += 10; return .handled }
            .onKeyPress(.upArrow)    { position.y -= 10; return .handled }
            .onKeyPress(.downArrow)  { position.y += 10; return .handled }
    }
}
```

`.onKeyPress` requires the view to be `focusable`. Return `.handled` if the view consumed the key, `.ignored` to let it bubble up.

---

## Apple Pencil and iPad

On iPad, Apple Pencil acts as a pointer device. Every drag gesture you have already written works with the Pencil automatically. Three Pencil-specific paths are worth knowing.

### Scribble

Scribble turns Pencil handwriting inside a `TextField` into typed text. It works with no code -- every standard text input supports it as soon as the user enables Scribble in Settings. You get it for free.

### PencilKit

`PKCanvasView` is UIKit, but bridges cleanly into SwiftUI for apps that want a drawing surface:

```swift
import PencilKit

struct Sketchpad: UIViewRepresentable {
    @Binding var drawing: PKDrawing

    func makeUIView(context: Context) -> PKCanvasView {
        let v = PKCanvasView()
        v.drawingPolicy = .anyInput
        v.delegate = context.coordinator
        v.drawing = drawing
        return v
    }

    func updateUIView(_ v: PKCanvasView, context: Context) {
        v.drawing = drawing
    }

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    final class Coordinator: NSObject, PKCanvasViewDelegate {
        let parent: Sketchpad
        init(_ parent: Sketchpad) { self.parent = parent }
        func canvasViewDrawingDidChange(_ canvas: PKCanvasView) {
            parent.drawing = canvas.drawing
        }
    }
}
```

Drop a `PKToolPicker` in front and you have a real sketching surface with pen, pencil, eraser, and color picker.

### Pencil Hover and Squeeze

Apple Pencil Pro adds hover (a preview before touching) and squeeze (a side-barrel gesture). Both reach SwiftUI through `onPencilSqueeze` and `onContinuousHover` on iOS 17.5 and later. Reach for these when the app benefits from a gesture the finger can't produce.

---

## Hit Targets and Accessibility

A touch is about 44 points wide. Interactive views should be at least 44x44 so users can actually hit them. Apple's Human Interface Guidelines publish this as the recommended minimum.

If your graphic is smaller, expand its tap area with `.contentShape`:

```swift
Image(systemName: "heart")
    .font(.system(size: 16))
    .frame(width: 44, height: 44)
    .contentShape(Rectangle())
    .onTapGesture { /* ... */ }
```

`.contentShape` tells SwiftUI which area counts for hit-testing, separate from the visible shape. The heart draws at 16-point but responds to taps anywhere in the 44x44 frame.

Every interactive view should also carry an accessibility label:

```swift
Image(systemName: "heart.fill")
    .onTapGesture { toggleFavorite() }
    .accessibilityLabel("Favorite")
    .accessibilityAddTraits(.isButton)
```

VoiceOver now announces the view as a button named "Favorite." Without the traits and label, it reads "heart.fill, image" -- useless.

---

## What Book 05 Does

Book 04 covered how the user talks to views. Book 05 takes it up one level: menus, navigation stacks, and `NavigationLink`. Once an app has more than one screen, the conversation is no longer about one gesture at a time; it's about moving between places.
