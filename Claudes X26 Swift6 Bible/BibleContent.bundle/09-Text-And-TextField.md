# Chapter 9: Text and TextField

## Text View Basics

`Text` is the workhorse for displaying read-only strings in SwiftUI.

```swift
Text("Hello, world")
Text(verbatim: "Hello, world") // skips localization lookup
```

Use `verbatim:` when you have a string that should never be localized (user-generated content, codes, etc.).

### String Interpolation

Standard Swift interpolation works inside `Text`:

```swift
Text("Score: \(score)")
Text("Price: \(price, format: .currency(code: "USD"))")
Text("Date: \(date, format: .dateTime.month().day())")
Text("Progress: \(value, format: .percent)")
```

The `format:` parameter is the modern way. It handles localization automatically.

### Markdown Support

`Text` parses inline Markdown out of the box when you use a string literal:

```swift
Text("This is **bold** and this is *italic*")
Text("Visit [Apple](https://apple.com)")
Text("Use `code` formatting")
Text("~~Strikethrough~~ text")
```

**Watch out:** Markdown parsing only works with string literals or `LocalizedStringKey`. If you pass a `String` variable, it renders as plain text:

```swift
let message = "This is **not bold**"
Text(message) // plain text, no markdown

// Fix: explicitly use LocalizedStringKey or AttributedString
Text(LocalizedStringKey(message)) // now it parses markdown
```

### Concatenating Text Views

You can combine `Text` views with `+`:

```swift
Text("Name: ").bold() + Text(userName).foregroundStyle(.secondary)
```

This is the only way to apply different styles to parts of the same line of text without using `AttributedString`.

---

## Text Modifiers

### Font

```swift
Text("Title").font(.title)
Text("Body").font(.body)
Text("Caption").font(.caption)
Text("Custom").font(.system(size: 24, weight: .bold, design: .rounded))
Text("Custom").font(.system(.title, design: .monospaced))
```

Built-in dynamic type sizes: `.largeTitle`, `.title`, `.title2`, `.title3`, `.headline`, `.subheadline`, `.body`, `.callout`, `.footnote`, `.caption`, `.caption2`.

Always prefer dynamic type over fixed sizes. It respects the user's accessibility settings.

### Color and Style

```swift
Text("Styled").foregroundStyle(.primary)
Text("Tinted").foregroundStyle(.blue)
Text("Gradient").foregroundStyle(.linearGradient(
    colors: [.blue, .purple],
    startPoint: .leading,
    endPoint: .trailing
))
```

`foregroundStyle` replaced `foregroundColor` (now deprecated). Use `foregroundStyle`.

### Weight and Emphasis

```swift
Text("Bold").bold()
Text("Italic").italic()
Text("Both").bold().italic()
Text("Light").fontWeight(.light)
Text("Heavy").fontWeight(.heavy)
Text("Wide").fontWidth(.expanded)
```

### Spacing: Kerning vs Tracking

```swift
Text("KERNING").kerning(2)   // adjusts space between character pairs
Text("TRACKING").tracking(2) // uniform spacing added to every character
```

**Practical difference:** `kerning` respects ligatures and pair-specific adjustments. `tracking` is uniform. For most UI work, `tracking` is what you want. For body text, `kerning` is more typographically correct.

**Watch out:** You cannot use both on the same `Text`. If you apply both, `kerning` is ignored.

### Line Limits and Truncation

```swift
Text("Long text here...")
    .lineLimit(2)
    .truncationMode(.tail) // .head, .middle, .tail

Text("Flexible")
    .lineLimit(1...5) // minimum 1 line, expand up to 5
```

### Baseline and Spacing

```swift
Text("Shifted").baselineOffset(5) // positive = up, negative = down
Text("Spaced").lineSpacing(8)     // extra space between lines
```

### Text Case

```swift
Text("hello").textCase(.uppercase) // "HELLO"
Text("HELLO").textCase(.lowercase) // "hello"
Text("hello").textCase(nil)        // no transformation
```

### Selection

Make text selectable by the user:

```swift
Text("Copy this").textSelection(.enabled)
```

---

## TextField

`TextField` is for single-line text input.

```swift
@State private var name = ""

TextField("Enter your name", text: $name)
```

The first argument is the prompt/placeholder text.

### Prompt Parameter

For more control over the placeholder:

```swift
TextField(text: $name, prompt: Text("Full name").foregroundStyle(.tertiary)) {
    Text("Name") // this is the label, used by accessibility
}
```

### Axis Parameter (Expanding TextField)

A `TextField` can expand vertically with the `axis` parameter:

```swift
TextField("Write something", text: $bio, axis: .vertical)
    .lineLimit(3...6) // starts at 3 lines, grows to 6
```

This gives you a text field that behaves like a growing text area. It starts compact and expands as the user types. Combine with `lineLimit` to control the range.

**Watch out:** Without `lineLimit`, an `axis: .vertical` text field will grow without bound.

### Keyboard Types

```swift
TextField("Email", text: $email)
    .keyboardType(.emailAddress)

TextField("Phone", text: $phone)
    .keyboardType(.phonePad)

TextField("Number", text: $amount)
    .keyboardType(.decimalPad)
```

Common types: `.default`, `.asciiCapable`, `.numberPad`, `.decimalPad`, `.phonePad`, `.emailAddress`, `.URL`, `.webSearch`.

### Autocapitalization

```swift
TextField("Name", text: $name)
    .textInputAutocapitalization(.words)
```

Options: `.never`, `.characters`, `.words`, `.sentences`.

**Watch out:** `.textInputAutocapitalization` replaced the old `.autocapitalization` modifier. Use the new one.

### Autocorrection

```swift
TextField("Username", text: $username)
    .autocorrectionDisabled(true)
```

### Text Content Type

Tells the system what kind of data this field collects, enabling autofill:

```swift
TextField("Email", text: $email)
    .textContentType(.emailAddress)

TextField("Street", text: $street)
    .textContentType(.streetAddressLine1)
```

### onSubmit

Fires when the user taps Return:

```swift
TextField("Search", text: $query)
    .onSubmit {
        performSearch()
    }
```

You can also set the return key label:

```swift
TextField("Search", text: $query)
    .submitLabel(.search) // .done, .go, .join, .next, .return, .search, .send
    .onSubmit { performSearch() }
```

### Formatting Input

Use `format:` for typed input that auto-formats:

```swift
@State private var amount: Double = 0

TextField("Amount", value: $amount, format: .currency(code: "USD"))
TextField("Percent", value: $percent, format: .percent)
TextField("Count", value: $count, format: .number)
```

**Watch out:** The binding updates only when the user commits (presses Return), not on every keystroke.

---

## SecureField

For password entry. Characters are hidden.

```swift
@State private var password = ""

SecureField("Password", text: $password)
    .textContentType(.password)
    .onSubmit { authenticate() }
```

`SecureField` supports the same modifiers as `TextField`: `.onSubmit`, `.submitLabel`, `.textContentType`, `.textInputAutocapitalization`, etc.

---

## @FocusState

Manage which field has keyboard focus programmatically.

### Boolean Focus (Single Field)

```swift
@FocusState private var isNameFocused: Bool

TextField("Name", text: $name)
    .focused($isNameFocused)

Button("Focus Name") {
    isNameFocused = true
}
```

### Enum Focus (Multiple Fields)

```swift
enum Field: Hashable {
    case firstName, lastName, email
}

@FocusState private var focusedField: Field?

Form {
    TextField("First", text: $first)
        .focused($focusedField, equals: .firstName)
        .onSubmit { focusedField = .lastName }

    TextField("Last", text: $last)
        .focused($focusedField, equals: .lastName)
        .onSubmit { focusedField = .email }

    TextField("Email", text: $email)
        .focused($focusedField, equals: .email)
        .onSubmit { submit() }
}
.onAppear { focusedField = .firstName }
```

This creates a tab-through flow: Return moves focus to the next field.

### Dismiss Keyboard

```swift
// Set focus to nil to dismiss keyboard
focusedField = nil
```

**Watch out:** `@FocusState` must be `Optional` when used with an enum (the `nil` state means nothing is focused). The boolean variant is non-optional.

**Watch out:** Setting focus in `onAppear` can be unreliable on first launch. If you need guaranteed focus on appear, wrap it in a brief task delay:

```swift
.task {
    try? await Task.sleep(for: .milliseconds(500))
    focusedField = .firstName
}
```

---

## Common Patterns

### Search Bar

```swift
@State private var searchText = ""
@FocusState private var searchFocused: Bool

HStack {
    Image(systemName: "magnifyingglass")
        .foregroundStyle(.secondary)

    TextField("Search", text: $searchText)
        .focused($searchFocused)
        .onSubmit { runSearch() }
        .submitLabel(.search)

    if !searchText.isEmpty {
        Button {
            searchText = ""
            searchFocused = true
        } label: {
            Image(systemName: "xmark.circle.fill")
                .foregroundStyle(.secondary)
        }
        .buttonStyle(.plain)
    }
}
.padding(8)
.background(.quaternary, in: .rect(cornerRadius: 10))
```

### Form with Validation

```swift
@State private var email = ""
@FocusState private var emailFocused: Bool

var emailIsValid: Bool {
    email.contains("@") && email.contains(".")
}

TextField("Email", text: $email)
    .focused($emailFocused)
    .keyboardType(.emailAddress)
    .textContentType(.emailAddress)
    .textInputAutocapitalization(.never)
    .autocorrectionDisabled()
    .overlay(alignment: .trailing) {
        if !email.isEmpty && !emailFocused {
            Image(systemName: emailIsValid ? "checkmark.circle" : "exclamationmark.circle")
                .foregroundStyle(emailIsValid ? .green : .red)
                .padding(.trailing, 8)
        }
    }
```

---

## Quick Reference

| Modifier | Purpose |
|---|---|
| `.font()` | Set text font |
| `.foregroundStyle()` | Set text color/style |
| `.bold()` / `.italic()` | Weight and emphasis |
| `.kerning()` / `.tracking()` | Letter spacing |
| `.lineLimit()` | Constrain line count |
| `.textCase()` | Force upper/lower case |
| `.textSelection()` | Enable copy |
| `.focused()` | Bind to @FocusState |
| `.onSubmit {}` | Handle Return key |
| `.submitLabel()` | Return key appearance |
| `.keyboardType()` | Keyboard layout |
| `.textInputAutocapitalization()` | Cap behavior |
| `.textContentType()` | Autofill hint |
| `.autocorrectionDisabled()` | Kill autocorrect |
