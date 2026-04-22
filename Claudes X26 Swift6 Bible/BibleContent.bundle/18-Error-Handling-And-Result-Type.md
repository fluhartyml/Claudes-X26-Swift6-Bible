# Chapter 18: Error Handling & Result Type

**Claude's Swift Reference 26** -- Part V: Advanced Techniques

---

## What You'll Learn

By the end of this chapter you can:

- Define custom error types with `enum` and the `Error` protocol.
- Throw errors from functions with `throws`, and handle them with `do` / `try` / `catch`.
- Understand the difference between `try`, `try?`, and `try!`, and when to reach for each.
- Use Swift 6's typed throws (`throws(MyError)`) to declare exactly which errors can escape a function.
- Use `Result<Success, Failure>` for callback-era APIs and cross-thread boundaries.

---

## Why Swift Throws Instead of Returning `nil`

Swift functions that might fail have two honest ways to say so:

1. Return an `Optional` -- "here's a value, or nothing."
2. Throw an error -- "here's a value, or a specific reason for the failure."

Optionals are great when there's only one failure mode and the reason doesn't matter. A dictionary lookup returning `nil` is fine -- the key either exists or it doesn't.

Errors are better when the caller needs to know **why** something failed: a file was missing, the network was down, the JSON was malformed. The error itself carries that story.

---

## Defining an Error Type

Any type conforming to the empty `Error` protocol can be thrown. Enums are the idiomatic choice:

```swift
enum ParseError: Error {
    case empty
    case notANumber(String)
    case outOfRange(value: Int, max: Int)
}
```

Associated values carry the details of the failure -- the offending string, the number that was out of range, whatever the caller needs to explain or recover.

For better error messages, conform to `LocalizedError`:

```swift
extension ParseError: LocalizedError {
    var errorDescription: String? {
        switch self {
        case .empty:
            return "Input was empty."
        case .notANumber(let s):
            return "\"\(s)\" isn't a number."
        case .outOfRange(let v, let max):
            return "\(v) is out of range (max \(max))."
        }
    }
}
```

Now printing the error or showing it to the user reads as plain prose.

---

## Throwing Errors

A function that might throw declares it with `throws`:

```swift
func parse(_ input: String, max: Int) throws -> Int {
    guard !input.isEmpty else {
        throw ParseError.empty
    }
    guard let n = Int(input) else {
        throw ParseError.notANumber(input)
    }
    guard n <= max else {
        throw ParseError.outOfRange(value: n, max: max)
    }
    return n
}
```

`throws` is part of the function's type. Callers have to acknowledge it with `try` or the compiler rejects the call.

Computed properties and initializers can throw too:

```swift
init(fromJSON data: Data) throws {
    // ...
}

var size: Int {
    get throws {
        // ...
    }
}
```

---

## Handling Errors

### do / try / catch

The default form is `do` / `try` / `catch`:

```swift
do {
    let value = try parse("42", max: 100)
    print("parsed:", value)
} catch ParseError.empty {
    print("input was empty")
} catch ParseError.notANumber(let s) {
    print("not a number:", s)
} catch {
    print("other:", error)
}
```

Catch clauses are patterns, just like `case` clauses in `switch`. A plain `catch` binds the error as `error` and acts as the catch-all. Swift checks that the `do` block's errors are all handled (or that the enclosing function also throws).

### try? -- Turn Errors into `nil`

When you don't care about the reason for failure:

```swift
let maybe = try? parse("abc", max: 100)   // Optional<Int>, nil on any throw
```

`try?` converts the call into an optional. Handy when you were going to check for `nil` anyway.

### try! -- Force It

When you're absolutely sure the call can't fail (and you want to trap if you're wrong):

```swift
let count = try! parse("42", max: 100)    // traps if parse throws
```

Use `try!` sparingly. It's appropriate for things like reading a file bundled with the app that you know exists. It's not appropriate for user input, network calls, or anything with uncertainty.

### Rethrowing

A function whose throwing behavior depends on a closure argument uses `rethrows`:

```swift
func retry<T>(_ body: () throws -> T) rethrows -> T {
    do   { return try body() }
    catch { return try body() }
}

let x = retry { 42 }                    // non-throwing closure: caller doesn't need try
let y = try retry { try parse("7", max: 10) } // throwing closure: caller needs try
```

`rethrows` keeps callers free of `try` when their closure isn't throwing.

---

## Typed Throws (Swift 6)

Swift 6 lets you declare exactly which error type a function throws:

```swift
func parse(_ input: String, max: Int) throws(ParseError) -> Int {
    guard !input.isEmpty else { throw .empty }
    guard let n = Int(input) else { throw .notANumber(input) }
    guard n <= max else { throw .outOfRange(value: n, max: max) }
    return n
}
```

Two things that change:

- Inside the function you can write `.empty` instead of `ParseError.empty` (Swift infers the type).
- The caller catches the concrete type without an `as?` cast:
  ```swift
  do {
      let v = try parse("42", max: 10)
  } catch let error: ParseError {
      // error is ParseError here, no cast needed
  }
  ```

Plain `throws` is shorthand for `throws(any Error)` -- "might throw anything." Use typed throws when your function has a fixed, bounded set of failures and you want the compiler to check that callers handle each one.

---

## Result -- The Errors-as-Values Type

`Result<Success, Failure>` is a standard-library enum with two cases:

```swift
public enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}
```

It represents the same information as a throwing function, but as a **value** you can pass around, store, and hand to a callback. Three common places you reach for it:

### 1. Callback-Based APIs

Older callback APIs (pre-`async`/`await`) use `Result` as the payload:

```swift
func fetch(completion: @escaping (Result<Data, NetworkError>) -> Void) {
    // ... some URLSession-style call
}

fetch { result in
    switch result {
    case .success(let data): print("got", data.count, "bytes")
    case .failure(let e):    print("failed:", e)
    }
}
```

### 2. Crossing Thread Boundaries

Throwing across a boundary can be awkward because errors don't flow easily across task or queue hops. Wrapping the value in `Result` turns it into something you can hand across the gap:

```swift
let result: Result<Int, Error> = .success(42)
DispatchQueue.main.async {
    handle(result)   // thread-safe: it's just a value
}
```

### 3. Converting Between Styles

`Result` has two convenience bridges:

```swift
// Throwing call → Result
let r = Result { try parse("42", max: 100) }

// Result → throwing
let n = try r.get()
```

`Result(_ body:)` runs the throwing closure and bundles the outcome; `.get()` re-throws the error out of the Result.

### When NOT to Use Result

In modern Swift code, prefer `async throws` over `Result` for anything new. `async throws` reads more naturally:

```swift
// Old
func fetch(completion: (Result<Data, Error>) -> Void)

// New
func fetch() async throws -> Data
```

Reach for `Result` when you're bridging to older callback APIs, storing the outcome, or sending it across a boundary that doesn't play well with throw.

---

## Chapter Mini-Example -- Parsing with Real Diagnostics

```swift
import SwiftUI

enum ParseError: LocalizedError {
    case empty
    case notANumber(String)
    case outOfRange(Int)

    var errorDescription: String? {
        switch self {
        case .empty:             return "Please enter a number."
        case .notANumber(let s): return "\"\(s)\" isn't a number."
        case .outOfRange(let n): return "\(n) is too big (max 100)."
        }
    }
}

func parse(_ raw: String) throws(ParseError) -> Int {
    guard !raw.isEmpty else { throw .empty }
    guard let n = Int(raw) else { throw .notANumber(raw) }
    guard n <= 100 else { throw .outOfRange(n) }
    return n
}

struct NumberInput: View {
    @State private var input = ""
    @State private var result: String = "—"
    @State private var error: String?

    var body: some View {
        Form {
            TextField("Enter a number up to 100", text: $input)
                .keyboardType(.numberPad)

            Button("Parse") {
                do {
                    let n = try parse(input)
                    result = "Got \(n)"
                    error  = nil
                } catch {
                    error = error.localizedDescription
                    result = "—"
                }
            }

            if let error {
                Label(error, systemImage: "exclamationmark.triangle.fill")
                    .foregroundStyle(.red)
            } else {
                Text(result)
            }
        }
    }
}
```

One throwing function, one typed error, one `do / catch`, real messages the user can actually act on. That's the full pattern; the rest is just more of it.

---

## What Book 19 Does

Errors are behavior that happens in response to bad input; Book 19 is about behavior you ship on purpose: custom views, custom modifiers, and the SwiftUI techniques that let you build your own widgets instead of always reaching for built-ins.
