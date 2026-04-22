"""
Real definitions and Swift examples for every entry in the Lexicon.

Each key maps to a dict with:
  - def: plain-English definition (2-4 sentences)
  - ex:  working Swift example (compiles under Swift 6)

Entries not in this dict fall back to the skeleton template in the generator.
"""

DEFS = {
    # ---------- A ----------
    'actor': {
        'def': "A reference type that protects its mutable state from data races by isolating it to its own execution context. Only one task at a time can touch an actor's stored properties; other callers suspend until their turn. You declare an actor with the `actor` keyword in place of `class`.",
        'ex': """actor Counter {
    private(set) var value = 0
    func increment() { value += 1 }
}

let counter = Counter()
await counter.increment()
let current = await counter.value
print(current) // 1"""
    },
    'any': {
        'def': "A keyword that marks an existential type — a box that holds any value conforming to a given protocol. `any Shape` means \"some value whose concrete type isn't known at compile time, only that it conforms to Shape.\" Swift requires `any` on existential uses of protocols with associated types or `Self` requirements.",
        'ex': """protocol Shape { func area() -> Double }

struct Square: Shape { let side: Double; func area() -> Double { side * side } }
struct Circle: Shape { let radius: Double; func area() -> Double { .pi * radius * radius } }

let shapes: [any Shape] = [Square(side: 2), Circle(radius: 3)]
for s in shapes { print(s.area()) }"""
    },
    'Any': {
        'def': "The universal type — an instance of `Any` can hold a value of any type at all, including class types, struct types, enums, function types, and optionals. Use it sparingly; reaching for `Any` usually means the type system has something more specific to offer.",
        'ex': """let bag: [Any] = [42, "hello", 3.14, true]

for item in bag {
    if let n = item as? Int {
        print("int: \\(n)")
    } else if let s = item as? String {
        print("string: \\(s)")
    }
}"""
    },
    'AnyObject': {
        'def': "A protocol that all class types implicitly conform to. Use it to constrain a generic or existential to class-only types, to interoperate with Objective-C APIs, or to form weak references without knowing the exact class.",
        'ex': """class Engine {}
class Car {}

let things: [AnyObject] = [Engine(), Car()]
print(type(of: things[0])) // Engine

// Class-only protocol requirement:
protocol Reference: AnyObject { var id: Int { get } }"""
    },
    'as': {
        'def': "A type-cast operator with three flavors: `as` for guaranteed upcasts checked at compile time, `as?` for a conditional downcast that returns an optional, and `as!` for a force downcast that traps if the types don't match.",
        'ex': """let values: [Any] = [1, "two", 3.0]

for v in values {
    if let s = v as? String {
        print("string: \\(s)")
    }
}

let anyNumber: Any = 42
let n = anyNumber as! Int // trap if wrong"""
    },
    'async': {
        'def': "A modifier that marks a function as asynchronous — able to suspend its execution and resume later without blocking its thread. Calling an async function requires `await` and must happen from another async context or a Task.",
        'ex': """func fetchUsername(id: Int) async -> String {
    try? await Task.sleep(nanoseconds: 200_000_000)
    return "user_\\(id)"
}

Task {
    let name = await fetchUsername(id: 7)
    print(name) // user_7
}"""
    },
    'await': {
        'def': "Marks the point where an async operation may suspend. Required in front of every call to an `async` function, an async property access, or an actor method call from outside the actor. The compiler won't let you forget it.",
        'ex': """func load() async -> String { "done" }

Task {
    print("before")
    let result = await load()
    print(result) // done
    print("after")
}"""
    },
    '@autoclosure': {
        'def': "An attribute that automatically wraps an argument expression in a closure, delaying its evaluation until the closure is called. Commonly used to make short-circuit and assertion-like APIs read naturally.",
        'ex': """func assertPositive(_ value: @autoclosure () -> Int) {
    let v = value()
    precondition(v > 0, "must be positive")
}

assertPositive(5)          // no parentheses — looks like a value
// assertPositive(-1)      // would trap"""
    },
    '@available': {
        'def': "An attribute that declares the platform, OS version, or Swift version a symbol is available on. The compiler uses it to gate access: you can't call an iOS 17+ API from code that still supports iOS 16 without checking `#available`.",
        'ex': """@available(iOS 17.0, macOS 14.0, *)
func newThing() { print("modern API") }

if #available(iOS 17.0, *) {
    newThing()
} else {
    print("fallback for older OS")
}"""
    },
    'Array': {
        'def': "An ordered, random-access collection of values of the same type, written as `[Element]`. Arrays are value types — assigning or passing an array makes a copy (with copy-on-write, so no work happens until a copy is actually mutated).",
        'ex': """var primes: [Int] = [2, 3, 5, 7]
primes.append(11)
print(primes.count)     // 5
print(primes[0])        // 2

let doubled = primes.map { $0 * 2 }
print(doubled)          // [4, 6, 10, 14, 22]"""
    },

    # ---------- B ----------
    'Bool': {
        'def': "The Boolean type — a value that is either `true` or `false`. It's the type of every condition Swift's control flow statements read (`if`, `while`, `guard`), and the result of comparison and logical operators.",
        'ex': """let isRaining = true
let hasUmbrella = false

if isRaining && !hasUmbrella {
    print("get wet")
} else {
    print("you're fine")
}"""
    },
    'break': {
        'def': "A control-flow statement that exits the enclosing loop or switch immediately. Inside nested loops, you can break to a labeled loop to exit more than one level at once.",
        'ex': """for n in 1...10 {
    if n == 5 { break }
    print(n)
}
// prints 1 2 3 4

outer: for row in 0..<3 {
    for col in 0..<3 {
        if row == col { break outer }
    }
}"""
    },
    '@Binding': {
        'def': "A SwiftUI property wrapper that creates a two-way connection to a value owned elsewhere — typically a `@State` in a parent view. Writing through a `@Binding` updates the source of truth, and the binding's reads always reflect the current source value.",
        'ex': """struct Toggle2: View {
    @Binding var isOn: Bool
    var body: some View {
        Button(isOn ? "On" : "Off") { isOn.toggle() }
    }
}

struct Parent: View {
    @State private var on = false
    var body: some View { Toggle2(isOn: $on) }
}"""
    },

    # ---------- C ----------
    'case': {
        'def': "Used in `switch` statements to match a pattern, in `enum` declarations to name one of the possible cases, and in `if case` / `for case` / `guard case` for pattern-matching outside `switch`.",
        'ex': """enum Direction { case north, south, east, west }

let heading = Direction.east
switch heading {
case .north: print("up")
case .south: print("down")
case .east, .west: print("sideways")
}"""
    },
    'catch': {
        'def': "Handles an error thrown from a `do` block. Each `catch` binds the error (by default as `error`) and can match specific cases with patterns. A `do/catch` must exhaustively handle the error types its body can throw.",
        'ex': """enum ParseError: Error { case bad, empty }

func parse(_ s: String) throws -> Int {
    if s.isEmpty { throw ParseError.empty }
    guard let n = Int(s) else { throw ParseError.bad }
    return n
}

do {
    let n = try parse("42")
    print(n)
} catch ParseError.empty {
    print("empty input")
} catch {
    print("other: \\(error)")
}"""
    },
    'Character': {
        'def': "A single human-readable character, which may be made of one or more Unicode scalars (e.g. an emoji with a skin-tone modifier is one `Character`). Strings iterate as sequences of `Character`, not bytes or scalars.",
        'ex': """let s = "Cafe\\u{301}" // 'e' + combining acute
for c in s { print(c) }
// C
// a
// f
// é  (one Character: e + ́ )
print(s.count) // 4"""
    },
    'class': {
        'def': "A reference type — multiple variables can refer to the same instance, and classes participate in inheritance and identity (`===`). Prefer `struct` unless you specifically need reference semantics, inheritance, deinitialization, or Objective-C interop.",
        'ex': """class Vehicle {
    var name: String
    init(name: String) { self.name = name }
}
class Car: Vehicle {
    var wheels = 4
}

let c = Car(name: "Chevy")
let alias = c
alias.name = "Ford"
print(c.name) // Ford — same instance"""
    },
    'closure': {
        'def': "A self-contained block of code you can pass around as a value. Closures capture any variables they reference from their surrounding scope. Functions, methods, and closures are all the same category in Swift — first-class values with a function type.",
        'ex': """let add: (Int, Int) -> Int = { a, b in a + b }
print(add(2, 3)) // 5

let names = ["Zoe", "Ada", "Max"]
let sorted = names.sorted { $0 < $1 }
print(sorted) // ["Ada", "Max", "Zoe"]"""
    },
    'Codable': {
        'def': "A typealias for `Encodable & Decodable`. A `Codable` type can be converted to and from external representations like JSON or property lists using `JSONEncoder` / `JSONDecoder`. Synthesis is automatic when every stored property is itself Codable.",
        'ex': """struct User: Codable {
    let id: Int
    let name: String
}

let u = User(id: 1, name: "Ada")
let data = try JSONEncoder().encode(u)
let back = try JSONDecoder().decode(User.self, from: data)
print(back.name) // Ada"""
    },
    'Collection': {
        'def': "A protocol for types that let you iterate multiple times over finite elements and access them by position. Arrays, Strings, Dictionaries, Sets, and Ranges all conform. Conforming types inherit dozens of algorithms (`map`, `filter`, `reduce`, `first(where:)`, etc.).",
        'ex': """func middle<C: Collection>(_ c: C) -> C.Element? where C.Index == Int {
    guard !c.isEmpty else { return nil }
    return c[c.count / 2]
}

print(middle([10, 20, 30]) ?? 0) // 20"""
    },
    'Comparable': {
        'def': "A protocol for types that define a total ordering via `<`. Conforming types get `>`, `<=`, `>=`, `sorted()`, `min()`, `max()`, and range expressions for free. Most built-in value types conform (`Int`, `Double`, `String`, `Date`).",
        'ex': """struct Score: Comparable {
    let value: Int
    static func < (a: Score, b: Score) -> Bool { a.value < b.value }
}

let scores = [Score(value: 88), Score(value: 42), Score(value: 95)]
print(scores.min()!.value) // 42
print(scores.sorted().map(\\.value)) // [42, 88, 95]"""
    },
    'continue': {
        'def': "A control-flow statement that skips the rest of the current loop iteration and jumps to the next one. Like `break`, it can target a labeled loop to continue an outer level.",
        'ex': """for n in 1...6 {
    if n.isMultiple(of: 2) { continue }
    print(n)
}
// prints 1 3 5"""
    },
    'convenience': {
        'def': "A modifier on a class initializer that means \"this init must delegate to another init of the same class, which eventually reaches a designated init.\" Convenience inits make common configurations simpler without the subclass having to override them.",
        'ex': """class Color {
    let red: Double, green: Double, blue: Double
    init(red: Double, green: Double, blue: Double) {
        self.red = red; self.green = green; self.blue = blue
    }
    convenience init(gray: Double) {
        self.init(red: gray, green: gray, blue: gray)
    }
}

let c = Color(gray: 0.5)"""
    },
    'CaseIterable': {
        'def': "A protocol for types — usually enums without associated values — that expose a static `allCases` collection of every case. Swift can synthesize the conformance for you; you only declare it.",
        'ex': """enum Direction: CaseIterable {
    case north, south, east, west
}

for d in Direction.allCases { print(d) }
print(Direction.allCases.count) // 4"""
    },

    # ---------- D ----------
    'defer': {
        'def': "Schedules a block of code to run when the current scope exits, no matter how it exits (return, throw, or falling off the end). Defers run in reverse order of appearance. Perfect for cleanup that must happen on every path.",
        'ex': """func withFile() {
    print("open")
    defer { print("close") } // always runs last
    print("work")
}

withFile()
// open
// work
// close"""
    },
    'deinit': {
        'def': "A class-only method that runs automatically just before an instance is deallocated. Use it to release resources the class owns — file handles, observers, C pointers. Deinit takes no parameters and can't be called directly.",
        'ex': """class Socket {
    init() { print("open socket") }
    deinit { print("close socket") }
}

do {
    let s = Socket()
    _ = s
}
// open socket
// close socket"""
    },
    'Decodable': {
        'def': "A protocol that describes a type that can be created from an external representation (like JSON). A decoder (e.g. `JSONDecoder`) reads the representation and produces an instance. Conformance is synthesized for types whose stored properties are all `Decodable`.",
        'ex': """struct Point: Decodable { let x: Double; let y: Double }

let json = #\"{ \"x\": 1.5, \"y\": 2.5 }\"#.data(using: .utf8)!
let p = try JSONDecoder().decode(Point.self, from: json)
print(p.x, p.y) // 1.5 2.5"""
    },
    'default': {
        'def': "The catch-all case in a `switch` statement, matched when no earlier case matches. Also the keyword for a default parameter value in a function declaration.",
        'ex': """func greet(_ name: String = "world") {
    print("Hello, \\(name)")
}
greet()          // Hello, world
greet("Michael") // Hello, Michael

switch 7 {
case 1: print("one")
case 2: print("two")
default: print("something else")
}"""
    },
    'Dictionary': {
        'def': "An unordered collection of key-value pairs, written as `[Key: Value]`. Keys must be `Hashable`. Lookups return an `Optional<Value>` since the key may not be present.",
        'ex': """var ages: [String: Int] = ["Ada": 30, "Max": 25]
ages["Zoe"] = 28

if let a = ages["Ada"] { print(a) } // 30

for (name, age) in ages.sorted(by: { $0.key < $1.key }) {
    print(name, age)
}"""
    },
    'do': {
        'def': "Starts a block. Used with `try`/`catch` to handle thrown errors, and on its own to introduce a nested scope (e.g. to limit the lifetime of shadowed bindings).",
        'ex': """do {
    let data = try Data(contentsOf: URL(fileURLWithPath: "/tmp/missing"))
    print(data.count)
} catch {
    print("failed: \\(error)")
}"""
    },
    'Double': {
        'def': "A 64-bit IEEE-754 floating-point type, Swift's default for non-integer numeric literals. Use `Double` when you need decimal values and don't specifically need the reduced precision of `Float`.",
        'ex': """let pi: Double = 3.14159265358979
let area = pi * 5 * 5
print(area) // 78.53981...

let x = 0.1 + 0.2 // 0.30000000000000004 — floating-point truth"""
    },
    'dynamic': {
        'def': "A modifier that forces a class member to be dispatched through the Objective-C runtime, which enables KVO and method swizzling. Only meaningful on classes that inherit from `NSObject` or bridge to Objective-C.",
        'ex': """import Foundation

class Player: NSObject {
    @objc dynamic var score = 0
}

let p = Player()
let obs = p.observe(\\.score, options: [.new]) { _, change in
    print("score is now \\(change.newValue ?? 0)")
}
p.score = 10 // score is now 10"""
    },
    '@discardableResult': {
        'def': "An attribute that suppresses the \"result of call is unused\" warning when callers ignore the return value. Use it for methods that mainly act for their side effect but also return something occasionally useful.",
        'ex': """@discardableResult
func logAndReturn(_ message: String) -> String {
    print(message)
    return message
}

logAndReturn("hi") // no warning even though we ignore the return"""
    },

    # ---------- E ----------
    'else': {
        'def': "The alternative branch of an `if`, `guard`, or `if let` / `guard let`. With `if`, execution falls through to the `else` when the condition is false; with `guard`, the `else` must exit the current scope.",
        'ex': """let n = 7
if n.isMultiple(of: 2) {
    print("even")
} else {
    print("odd")
}

func first(_ a: [Int]) -> Int {
    guard let v = a.first else { return -1 }
    return v
}"""
    },
    'Encodable': {
        'def': "A protocol that describes a type that can be converted to an external representation (like JSON or a property list). An encoder (e.g. `JSONEncoder`) writes the representation. Synthesis is automatic when every stored property is `Encodable`.",
        'ex': """struct Point: Encodable { let x: Double; let y: Double }

let p = Point(x: 1.5, y: 2.5)
let data = try JSONEncoder().encode(p)
print(String(data: data, encoding: .utf8)!)
// {"x":1.5,"y":2.5}"""
    },
    'enum': {
        'def': "A value type that defines a common set of related values. Cases can carry associated values of different types, cases can have a common raw type (like `String` or `Int`), and methods / computed properties can hang off the enum. Enums are the Swift way to model \"one of several shapes.\"",
        'ex': """enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}

let r: Result<Int, Error> = .success(42)
switch r {
case .success(let v): print(v)
case .failure(let e): print(e)
}"""
    },
    'Equatable': {
        'def': "A protocol for types that support `==` and `!=`. Swift synthesizes conformance for structs whose properties are all `Equatable` and for enums whose associated values are all `Equatable`.",
        'ex': """struct Point: Equatable { let x, y: Int }

let a = Point(x: 1, y: 2)
let b = Point(x: 1, y: 2)
print(a == b) // true"""
    },
    'Error': {
        'def': "The empty protocol that every error type conforms to. You throw any value whose type conforms to `Error` — usually an enum that models the failure modes of a particular operation.",
        'ex': """enum NetworkError: Error {
    case offline
    case badStatus(Int)
}

func fetch() throws {
    throw NetworkError.badStatus(500)
}

do { try fetch() }
catch NetworkError.badStatus(let code) { print("HTTP \\(code)") }
catch { print(error) }"""
    },
    'extension': {
        'def': "Adds computed properties, instance / type methods, initializers, nested types, or protocol conformances to an existing type — even one you don't own. Extensions can't add stored properties.",
        'ex': """extension Int {
    var isEven: Bool { self.isMultiple(of: 2) }
    func times(_ body: () -> Void) {
        for _ in 0..<self { body() }
    }
}

print(6.isEven) // true
3.times { print("hi") }"""
    },
    '@escaping': {
        'def': "An attribute on a closure parameter that declares the closure may outlive the function call — stored in a property, added to an array, dispatched asynchronously. Non-escaping is the default; Swift needs `@escaping` to know the closure can't assume `self` is still around.",
        'ex': """var handlers: [() -> Void] = []

func register(_ handler: @escaping () -> Void) {
    handlers.append(handler)
}

register { print("fired") }
handlers.first?()"""
    },
    '@Environment': {
        'def': "A SwiftUI property wrapper that reads a value from the view's environment — values like color scheme, locale, dismiss actions, or custom keys. Changes to the environment re-trigger the view's body.",
        'ex': """struct ThemedLabel: View {
    @Environment(\\.colorScheme) var scheme
    var body: some View {
        Text("Hello")
            .foregroundStyle(scheme == .dark ? .white : .black)
    }
}"""
    },
    '@EnvironmentObject': {
        'def': "A SwiftUI property wrapper that reads an `ObservableObject` put into the environment by an ancestor view via `.environmentObject(_:)`. If no ancestor supplied one, the app traps at runtime.",
        'ex': """final class Session: ObservableObject { @Published var username = "" }

struct Root: View {
    @StateObject private var session = Session()
    var body: some View { Inner().environmentObject(session) }
}
struct Inner: View {
    @EnvironmentObject var session: Session
    var body: some View { Text(session.username) }
}"""
    },
    'ExpressibleByStringLiteral': {
        'def': "A protocol that lets a type be initialized directly from a string literal. Conform and Swift will let callers pass `\"…\"` anywhere your type is expected.",
        'ex': """struct Tag: ExpressibleByStringLiteral {
    let raw: String
    init(stringLiteral value: String) { self.raw = value }
}

let t: Tag = "swift"
print(t.raw) // swift"""
    },
    '#elseif': {
        'def': "A compile-time conditional directive used alongside `#if` and `#else` to compile different code on different platforms, architectures, configurations, or Swift versions.",
        'ex': """#if os(iOS)
    let platform = "iOS"
#elseif os(macOS)
    let platform = "macOS"
#else
    let platform = "other"
#endif

print(platform)"""
    },
    '#endif': {
        'def': "Closes a `#if` / `#elseif` / `#else` conditional-compilation block. Every `#if` needs a matching `#endif`.",
        'ex': """#if DEBUG
    print("debug build")
#endif"""
    },
    '#error': {
        'def': "Emits a compile-time error with the given message. Use it inside a conditional-compilation branch to refuse to compile a configuration that isn't supported.",
        'ex': """#if !canImport(Foundation)
    #error("This module requires Foundation")
#endif"""
    },

    # ---------- F ----------
    'fallthrough': {
        'def': "Inside a `switch`, falls through to execute the next case's body without checking its pattern. Swift cases do NOT fall through by default; you have to ask with this keyword.",
        'ex': """let n = 1
switch n {
case 1:
    print("one")
    fallthrough
case 2:
    print("also runs")
default:
    break
}
// one
// also runs"""
    },
    'false': {
        'def': "One of the two `Bool` literal values, representing logical falsehood. The other is `true`.",
        'ex': """let isReady: Bool = false
if !isReady { print("keep waiting") }"""
    },
    'fileprivate': {
        'def': "An access level that makes a declaration visible everywhere in the file that declares it. Use it to share implementation between types or extensions that live in the same file but need to stay hidden from the rest of the module.",
        'ex': """// Inside One.swift
fileprivate let secret = "shh"

struct Visible {
    var exposed: String { secret } // same file: allowed
}"""
    },
    'final': {
        'def': "A class modifier that forbids subclassing the class, or overriding the marked member. Apply it whenever you don't intend a class to be extended — the compiler can then devirtualize calls for speed and the code reads as closed-for-extension.",
        'ex': """final class Logger {
    func log(_ s: String) { print(s) }
}

// class Sub: Logger {} // error: inheritance from a final class"""
    },
    'Float': {
        'def': "A 32-bit IEEE-754 floating-point type. Use `Double` by default; reach for `Float` only when memory or bandwidth for huge arrays of floats matters (e.g. graphics, audio buffers).",
        'ex': """let x: Float = 1.5
let y: Float = 2.5
print(x + y) // 4.0

// Type context matters:
let whole: Float = 0.1 + 0.2 // still imprecise, just 32-bit"""
    },
    'for': {
        'def': "Iterates over a sequence — arrays, ranges, strings, dictionaries, or anything conforming to `Sequence`. The `for-in` form binds each element to a constant; `for case` adds pattern matching.",
        'ex': """for i in 1...5 { print(i) }

let names = ["Ada", "Max", "Zoe"]
for name in names where name.count > 2 { print(name) }

// for case — only iterate matching cases:
let results: [Result<Int, Error>] = [.success(1), .failure(NSError()), .success(3)]
for case .success(let v) in results { print(v) }
// 1
// 3"""
    },
    'func': {
        'def': "Declares a function — a named, reusable unit of code. Functions can take parameters, return a value, be generic, throw errors, be async, and accept trailing closures.",
        'ex': """func greet(_ name: String, loud: Bool = false) -> String {
    let text = "hello, \\(name)"
    return loud ? text.uppercased() : text
}

print(greet("Ada"))
print(greet("Max", loud: true))"""
    },
    '@frozen': {
        'def': "An attribute promising that the type's layout or set of cases won't change in future versions of the module. Lets the compiler make optimizations that would otherwise be unsafe across library-evolution boundaries.",
        'ex': """@frozen public enum Either<A, B> {
    case left(A)
    case right(B)
}

let e: Either<Int, String> = .left(7)"""
    },
    '@FocusState': {
        'def': "A SwiftUI property wrapper that binds to the currently-focused form control. Write to it to programmatically move focus; read it to tell which field is focused.",
        'ex': """struct LoginForm: View {
    enum Field { case username, password }
    @FocusState private var focus: Field?
    @State private var u = "", p = ""

    var body: some View {
        VStack {
            TextField("user", text: $u).focused($focus, equals: .username)
            SecureField("pw", text: $p).focused($focus, equals: .password)
            Button("Go") { focus = .username }
        }
    }
}"""
    },
    '#file': {
        'def': "A magic literal that expands to the source file path where it appears. Useful in assertions and logging to identify the caller without hand-writing the filename.",
        'ex': """func logHere(_ message: String, file: StaticString = #file, line: UInt = #line) {
    print("[\\(file):\\(line)] \\(message)")
}

logHere("reached") // logs the file + line of the call site"""
    },
    '#function': {
        'def': "A magic literal that expands to the name of the enclosing function (or property, or initializer). Useful in logging, assertions, and tracing.",
        'ex': """func doWork() {
    print(#function) // "doWork()"
}

doWork()"""
    },

    # ---------- G ----------
    'generic': {
        'def': "Code that works with a placeholder type parameter rather than a specific concrete type. Generics let you write one `Stack<Element>` instead of one stack per element type, while keeping full type safety at each use site.",
        'ex': """func pairUp<T>(_ a: T, _ b: T) -> [T] { [a, b] }

print(pairUp(1, 2))        // [1, 2]
print(pairUp("hi", "bye")) // ["hi", "bye"]

struct Stack<Element> {
    private var items: [Element] = []
    mutating func push(_ x: Element) { items.append(x) }
    mutating func pop() -> Element? { items.popLast() }
}"""
    },
    'get': {
        'def': "Defines the read accessor of a computed property or subscript. Paired with `set` for read/write; stand-alone `get` (without `set`) defines a read-only computed property.",
        'ex': """struct Rectangle {
    var width: Double, height: Double
    var area: Double {
        get { width * height }
    }
}

let r = Rectangle(width: 3, height: 4)
print(r.area) // 12.0"""
    },
    'guard': {
        'def': "An early-exit statement. Its condition must be true to keep going; if it's false, the `else` block runs and must leave the current scope (return, throw, break, continue, or trap). Bindings made in the condition are visible after the `guard`.",
        'ex': """func firstName(from full: String) -> String? {
    let parts = full.split(separator: " ")
    guard let first = parts.first else { return nil }
    return String(first)
}

print(firstName(from: "Ada Lovelace") ?? "?") // Ada"""
    },
    '@GestureState': {
        'def': "A SwiftUI property wrapper that holds gesture state and automatically resets to its initial value when the gesture ends or is cancelled. Prevents leftover state from a gesture you aborted.",
        'ex': """struct DragSquare: View {
    @GestureState private var drag: CGSize = .zero
    var body: some View {
        Rectangle().frame(width: 80, height: 80)
            .offset(drag)
            .gesture(DragGesture()
                .updating($drag) { v, s, _ in s = v.translation })
    }
}"""
    },

    # ---------- H ----------
    'Hashable': {
        'def': "A protocol for types that can produce an integer hash value, which lets them be used as Dictionary keys, Set members, and in any context needing content-based identity. Swift synthesizes conformance for value types whose properties are all `Hashable`.",
        'ex': """struct Coord: Hashable { let x, y: Int }

var visited: Set<Coord> = []
visited.insert(Coord(x: 0, y: 0))
visited.insert(Coord(x: 0, y: 0)) // duplicate — no-op
print(visited.count) // 1"""
    },

    # ---------- I ----------
    'if': {
        'def': "Conditionally runs a block. Swift's `if` also has expression form — `let x = if cond { 1 } else { 2 }` — and combines with `let`/`var` for optional unwrapping and with `case` for pattern matching.",
        'ex': """let n = 7
let label = if n > 0 { "positive" }
            else if n < 0 { "negative" }
            else { "zero" }
print(label) // positive

let maybe: Int? = 3
if let v = maybe { print(v) }"""
    },
    'import': {
        'def': "Makes the public API of another module available in the current source file. Modules include Apple's frameworks (`Foundation`, `SwiftUI`), SwiftPM packages, and submodules inside the current app.",
        'ex': """import Foundation
import SwiftUI

let now = Date()
print(now)"""
    },
    'in': {
        'def': "Separates a closure's signature from its body, and separates a loop variable from its sequence in `for-in`.",
        'ex': """let squares = (1...5).map { n in n * n }
print(squares) // [1, 4, 9, 16, 25]

for name in ["Ada", "Max"] { print(name) }"""
    },
    'indirect': {
        'def': "Marks an enum or individual enum case whose associated value stores another instance of that enum. Without `indirect`, the enum would have infinite size; `indirect` tells Swift to box the recursive case behind a pointer.",
        'ex': """indirect enum List<T> {
    case empty
    case node(T, List<T>)
}

let l: List<Int> = .node(1, .node(2, .node(3, .empty)))"""
    },
    'infix': {
        'def': "Declares that a custom operator sits between its two operands (like `+`, `==`, `..<`). Without `infix`, the compiler doesn't know how to parse your operator.",
        'ex': """infix operator **: MultiplicationPrecedence

func ** (base: Int, exp: Int) -> Int {
    var r = 1
    for _ in 0..<exp { r *= base }
    return r
}

print(2 ** 10) // 1024"""
    },
    'init': {
        'def': "A class / struct / enum initializer — the method that sets up a new instance. Swift checks that every stored property is initialized before the initializer returns. Initializers can throw, be `required`, `convenience`, or `failable` (`init?`).",
        'ex': """struct User {
    let name: String
    let age: Int
    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }
    init(anonymousWithAge age: Int) {
        self.init(name: "anonymous", age: age)
    }
}"""
    },
    'inout': {
        'def': "Marks a function parameter as pass-by-reference: the function can mutate it, and the change is visible to the caller after the call returns. At the call site, prefix the argument with `&`.",
        'ex': """func doubleIt(_ n: inout Int) {
    n *= 2
}

var x = 5
doubleIt(&x)
print(x) // 10"""
    },
    'Int': {
        'def': "Swift's default signed integer type. Its size matches the platform's native word size (64-bit on modern Apple hardware). Use `Int` for indexes and counts unless you have a specific reason to pin a width.",
        'ex': """let count: Int = 42
let sum = (1...100).reduce(0, +)
print(sum) // 5050"""
    },
    'internal': {
        'def': "The default access level — a declaration is visible everywhere in the module that declares it, and invisible from the outside. You rarely write `internal` because it's implicit.",
        'ex': """// Inside MyLib.swift (module MyLib)
internal struct Cache { var items: [String] = [] }
// Equivalent:
struct Cache2 { var items: [String] = [] }"""
    },
    'is': {
        'def': "A runtime type-check operator. `value is Type` returns `true` when `value` is an instance of `Type` (or a subclass, or a type conforming to the protocol).",
        'ex': """let items: [Any] = [1, "two", 3.0]
let strings = items.filter { $0 is String }
print(strings.count) // 1

if items[1] is String { print("element 1 is a String") }"""
    },
    'Identifiable': {
        'def': "A protocol for types that have a stable `id`. SwiftUI's `ForEach`, `List`, and similar APIs use `Identifiable` so they can track elements across updates. Any `Hashable`, stable property can serve as the `id`.",
        'ex': """struct Todo: Identifiable {
    let id: UUID = UUID()
    var title: String
}

let todos = [Todo(title: "buy milk"), Todo(title: "write book")]
// in a SwiftUI view:
// List(todos) { todo in Text(todo.title) }"""
    },
    '@inlinable': {
        'def': "An attribute that promises a public function's body won't change incompatibly, letting callers in other modules inline the body across module boundaries. Commonly used in small, hot-path library code.",
        'ex': """@inlinable
public func clamp<T: Comparable>(_ x: T, min lo: T, max hi: T) -> T {
    return x < lo ? lo : (x > hi ? hi : x)
}"""
    },

    # ---------- J ----------
    'JSONEncoder': {
        'def': "A Foundation class that turns a `Encodable` value into JSON `Data`. You configure its output format (pretty-printed, sorted keys, date strategy) once and reuse the instance. Pair with `JSONDecoder` to round-trip.",
        'ex': """import Foundation

struct User: Codable { let id: Int; let name: String }

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

let user = User(id: 7, name: "Ada")
let data = try encoder.encode(user)
print(String(data: data, encoding: .utf8) ?? "")"""
    },
    'JSONDecoder': {
        'def': "A Foundation class that reads JSON `Data` back into an `Decodable` type. Configure how it interprets dates, keys, and raw numbers once, then reuse. The dual of `JSONEncoder`.",
        'ex': """import Foundation

struct User: Codable { let id: Int; let name: String }

let json = #\"{ \"id\": 7, \"name\": \"Ada\" }\"#.data(using: .utf8)!
let user = try JSONDecoder().decode(User.self, from: json)
print(user.name) // Ada"""
    },
    'JSONSerialization': {
        'def': "The lower-level Foundation API for JSON, predating `Codable`. It converts between `Data` and untyped `Any` / `[String: Any]` / `[Any]` — useful when you don't have (or want) a Swift type and just need to inspect a JSON payload.",
        'ex': """import Foundation

let raw = #\"{ \"ok\": true, \"count\": 3, \"items\": [\"a\", \"b\"] }\"#
    .data(using: .utf8)!

let obj = try JSONSerialization.jsonObject(with: raw) as? [String: Any]
if let count = obj?[\"count\"] as? Int { print(count) } // 3"""
    },

    # ---------- K ----------
    'KeyPath': {
        'def': "A type-safe, compiler-checked reference to a property of a type, written `\\Type.property`. Use key paths with `map`, `sorted(by:)`, SwiftUI bindings, and property observation APIs.",
        'ex': """struct User { let name: String; let age: Int }

let users = [User(name: "Ada", age: 30), User(name: "Max", age: 25)]
let names = users.map(\\.name)
let byAge = users.sorted { $0.age < $1.age }
print(names)                  // ["Ada", "Max"]
print(byAge.first?.name ?? "") // Max"""
    },

    # ---------- L ----------
    'lazy': {
        'def': "A modifier that delays a stored property's initialization until the first time it's read. The initializer runs once, ever. `lazy` can only be used on stored properties of classes / structs declared with `var`, and the containing type must be mutable for the first read.",
        'ex': """struct Report {
    lazy var expensive: [Int] = {
        print("computing")
        return (1...1_000).map { $0 * $0 }
    }()
}

var r = Report()
print(r.expensive.last!) // prints "computing" then 1000000
print(r.expensive.last!) // just prints 1000000 — cached"""
    },
    'let': {
        'def': "Declares a constant — a binding whose value can't be reassigned. `let` doesn't mean the referenced object is deeply immutable (a `let` on a class reference still lets you mutate the instance's properties); it means the binding itself is fixed.",
        'ex': """let pi = 3.14159
// pi = 3.14 // error: cannot assign

let array = [1, 2, 3]
// array.append(4) // error — arrays are value types, let forbids mutation

let view = UIView()   // let on a class
// view = UIView()   // error: cannot reassign
view.backgroundColor = .red // allowed — mutating the instance"""
    },
    '#line': {
        'def': "A magic literal that expands to the line number where it appears, in the file where it appears. Useful as a default parameter value for logging / assertion helpers.",
        'ex': """func here(file: StaticString = #file, line: UInt = #line) {
    print("at \\(file):\\(line)")
}

here() // prints this file and this line"""
    },

    # ---------- M ----------
    'map': {
        'def': "A method on Sequence (and Optional, and Result) that transforms every element by a closure, returning a new collection (or Optional / Result) of the transformed values. Does not mutate the source.",
        'ex': """let squares = (1...5).map { $0 * $0 }
print(squares) // [1, 4, 9, 16, 25]

let maybe: Int? = 5
let doubled = maybe.map { $0 * 2 } // Optional(10)"""
    },
    'mutating': {
        'def': "A modifier on a struct / enum method that tells Swift the method may change `self`'s stored properties. You can only call `mutating` methods on variables (`var`), not constants.",
        'ex': """struct Counter {
    var value = 0
    mutating func increment() { value += 1 }
}

var c = Counter()
c.increment()
print(c.value) // 1

// let constant = Counter()
// constant.increment() // error: mutating on let"""
    },
    '@main': {
        'def': "An attribute on a type (usually a struct) that designates it as the program's entry point. The type must provide a `static func main()` or conform to a protocol that supplies one (like `App` in SwiftUI).",
        'ex': """@main
struct Program {
    static func main() {
        print("hello, command line")
    }
}"""
    },
    '@MainActor': {
        'def': "An attribute that binds a type, function, or property to the main actor — the one that owns the UI. Calls to `@MainActor` work from another isolation context require `await`. Apply it to ensure UI code never runs off the main thread.",
        'ex': """@MainActor
final class ViewModel: ObservableObject {
    @Published var title = "loading"
}

// From a background task:
Task {
    let model = await ViewModel()
    await MainActor.run { model.title = "ready" }
}"""
    },

    # ---------- N ----------
    'Never': {
        'def': "The type of values that never exist. A function returning `Never` doesn't return — it aborts (`fatalError`), exits (`exit`), or loops forever. Because `Never` has no values, it converts to anything, which is useful in exhaustive switches.",
        'ex': """func crash(_ reason: String) -> Never {
    fatalError(reason)
}

func pickNumber(_ n: Int) -> String {
    switch n {
    case 1: return "one"
    case 2: return "two"
    default: crash("unexpected \\(n)")
    }
}"""
    },
    'nil': {
        'def': "The absence of a value for an Optional type. `nil` is not zero, and it's not a pointer — it's a discriminator that says \"this Optional is the `.none` case.\" Only Optional types can be `nil`.",
        'ex': """var name: String? = "Ada"
name = nil

if name == nil {
    print("no name")
}

let count: Int? = nil
let doubled = count.map { $0 * 2 } ?? 0
print(doubled) // 0"""
    },
    'nonmutating': {
        'def': "A modifier on a property setter (inside a struct / enum) that promises the set operation doesn't change `self`. Useful when a computed setter writes to external storage rather than back into `self`.",
        'ex': """struct Cache {
    nonmutating set(_ value: String) {
        UserDefaults.standard.set(value, forKey: "note")
    }
    init() {}
}

extension Cache {
    var note: String {
        get { UserDefaults.standard.string(forKey: "note") ?? "" }
        nonmutating set { UserDefaults.standard.set(newValue, forKey: "note") }
    }
}"""
    },

    # ---------- O ----------
    'open': {
        'def': "The most permissive access level — a declaration is visible AND subclassable / overridable from other modules. Use it for library types you explicitly intend consumers to extend.",
        'ex': """open class Widget {
    open func draw() { print("base draw") }
}

// In another module:
// class Fancy: Widget {
//     override func draw() { print("fancy") }
// }"""
    },
    'operator': {
        'def': "Declares a custom operator token at the top level. You must choose its fixity (`prefix`, `infix`, `postfix`) and, for `infix`, a precedence group.",
        'ex': """prefix operator √

prefix func √ (x: Double) -> Double { x.squareRoot() }

print(√16) // 4.0"""
    },
    'Optional': {
        'def': "A generic enum with two cases, `.some(value)` and `.none`, used to model \"a value, or nothing.\" Writing `T?` is shorthand for `Optional<T>`. Unwrap with `if let`, `guard let`, `??`, `map`, `flatMap`, or (cautiously) `!`.",
        'ex': """let name: String? = "Ada"

if let n = name { print(n) }           // Ada
let length = name?.count ?? 0          // 3
let explicitly: Optional<Int> = .some(42)
print(explicitly ?? -1)                // 42"""
    },
    'override': {
        'def': "A modifier on a method, property, or subscript that replaces the inherited version from a superclass. Swift requires `override` so you can't shadow a superclass member by accident.",
        'ex': """class Animal { func speak() { print("...") } }
class Dog: Animal {
    override func speak() { print("woof") }
}

let d: Animal = Dog()
d.speak() // woof"""
    },
    '@objc': {
        'def': "Exposes a Swift declaration to the Objective-C runtime. Required for KVO, selectors, and dynamic dispatch through the ObjC runtime. Often combined with `dynamic`. Use only when you actually need ObjC interop.",
        'ex': """import Foundation

class Button: NSObject {
    @objc func tap() { print("tapped") }
}

let b = Button()
b.perform(#selector(Button.tap))"""
    },
    '@Observable': {
        'def': "A macro (Swift 5.9+) that turns a class into an observable model: all stored properties automatically participate in change tracking and SwiftUI views re-render when they change. Replaces the older `ObservableObject` / `@Published` pattern.",
        'ex': """import Observation

@Observable
final class Counter {
    var value = 0
    func inc() { value += 1 }
}

// In a SwiftUI View:
// @State var counter = Counter()
// Text("\\(counter.value)")  // view updates when value changes"""
    },
    '@ObservedObject': {
        'def': "A SwiftUI property wrapper that subscribes a view to an `ObservableObject` owned elsewhere. The view redraws when any `@Published` property changes. Use `@StateObject` when the view creates the object; use `@ObservedObject` when it's passed in.",
        'ex': """final class Model: ObservableObject {
    @Published var count = 0
}

struct Row: View {
    @ObservedObject var model: Model
    var body: some View {
        Button("tap \\(model.count)") { model.count += 1 }
    }
}"""
    },

    # ---------- P ----------
    'postfix': {
        'def': "Declares that a custom operator appears after its operand (like `!` in `optional!`). Without `postfix`, the compiler can't parse the operator.",
        'ex': """postfix operator ++

postfix func ++ (x: inout Int) -> Int {
    defer { x += 1 }
    return x
}

var n = 5
let before = n++
print(before, n) // 5 6"""
    },
    'precedencegroup': {
        'def': "Declares a named precedence group — the binding strength and associativity that an `infix` operator belongs to. Rarely needed unless you're building a DSL; usually you reuse existing groups like `AdditionPrecedence`.",
        'ex': """precedencegroup PowerPrecedence {
    higherThan: MultiplicationPrecedence
    associativity: right
}

infix operator ** : PowerPrecedence

func ** (base: Int, exp: Int) -> Int {
    var r = 1
    for _ in 0..<exp { r *= base }
    return r
}

print(2 ** 3 * 4) // 32 — ** binds tighter than *"""
    },
    'prefix': {
        'def': "Declares that a custom operator appears before its operand (like `!` in `!bool` or `-` in `-5`). Needed alongside the operator-function declaration.",
        'ex': """prefix operator ¬

prefix func ¬ (b: Bool) -> Bool { !b }

print(¬true) // false"""
    },
    'print': {
        'def': "Writes its arguments to standard output, followed by a newline by default. Each argument is stringified via its `String(describing:)` form. Handy for quick debugging and console tools.",
        'ex': """print("hello")
print("x =", 42)
print("joined", "words", separator: "-") // joined-words
print("no newline", terminator: "")
print(" continued")"""
    },
    'private': {
        'def': "The most restrictive access level — visible only within the enclosing declaration and the same-file extensions of it. Use it to hide implementation details and protect invariants.",
        'ex': """struct BankAccount {
    private var balance: Double = 0
    mutating func deposit(_ amount: Double) { balance += amount }
    var formatted: String { String(format: "$%.2f", balance) }
}

var a = BankAccount()
a.deposit(10)
// a.balance        // error: private
print(a.formatted) // $10.00"""
    },
    'protocol': {
        'def': "Declares a set of requirements — methods, properties, associated types — that a conforming type must satisfy. Protocols are Swift's way of expressing capabilities and abstractions without inheritance hierarchies.",
        'ex': """protocol Greeter {
    func greet(_ name: String) -> String
}

struct Polite: Greeter {
    func greet(_ name: String) -> String { "Hello, \\(name)." }
}

let g: Greeter = Polite()
print(g.greet("Ada")) // Hello, Ada."""
    },
    '@Published': {
        'def': "A property wrapper on a property of an `ObservableObject` that emits an update on the object's `objectWillChange` publisher just before the value changes. SwiftUI views subscribed to the object re-render on that signal.",
        'ex': """import Combine

final class Counter: ObservableObject {
    @Published var value = 0
}

// In a SwiftUI View:
// @ObservedObject var counter: Counter
// Text("\\(counter.value)")"""
    },
    'public': {
        'def': "An access level that makes a declaration visible from outside the module but not subclassable or overridable unless you also mark it `open`. Use `public` for library API that callers may use but shouldn't extend.",
        'ex': """public struct Point {
    public let x, y: Double
    public init(x: Double, y: Double) {
        self.x = x; self.y = y
    }
}"""
    },
    '#Predicate': {
        'def': "A freestanding macro (Swift 5.9+) that builds a `Predicate<Input>` — a structured, introspectable filter expression — from a closure-like body. Used with SwiftData, CoreData via interop, and generic predicate-aware APIs.",
        'ex': """import Foundation

struct Item { let name: String; let price: Double }

let cheap = #Predicate<Item> { $0.price < 10 }
let items = [Item(name: "pen", price: 2), Item(name: "chair", price: 50)]
let matches = try items.filter { try cheap.evaluate($0) }
print(matches.count) // 1"""
    },
    '#Preview': {
        'def': "A freestanding macro (Xcode 15+) that declares a SwiftUI preview without boilerplate. Multiple `#Preview` blocks can sit in one file, each showing a different configuration.",
        'ex': """import SwiftUI

struct Hello: View {
    var body: some View { Text("hi") }
}

#Preview { Hello() }
#Preview("Dark") { Hello().preferredColorScheme(.dark) }"""
    },

    # ---------- Q ----------
    '@Query': {
        'def': "A SwiftData property wrapper that fetches a live, auto-updating collection of model objects from the model context. Views with `@Query` redraw automatically when matching data changes.",
        'ex': """import SwiftData
import SwiftUI

@Model final class Note { var title: String = ""; init(title: String) { self.title = title } }

struct NotesList: View {
    @Query(sort: \\.title) var notes: [Note]
    var body: some View {
        List(notes) { Text($0.title) }
    }
}"""
    },

    # ---------- R ----------
    'Range': {
        'def': "A half-open range of Comparable values, written `a..<b`, meaning all values from `a` up to but not including `b`. `Range` is empty when `a == b`.",
        'ex': """let r = 0..<5
print(r.count)     // 5
print(Array(r))    // [0, 1, 2, 3, 4]
print(r.contains(5)) // false"""
    },
    'ClosedRange': {
        'def': "A range that includes both endpoints, written `a...b`. Unlike `Range`, you can never have an empty `ClosedRange` — `a...a` contains one element.",
        'ex': """let r = 1...5
print(r.count)     // 5
print(Array(r))    // [1, 2, 3, 4, 5]
print(r.contains(5)) // true"""
    },
    'RawRepresentable': {
        'def': "A protocol for types that are interchangeable with an associated `RawValue` (often `Int` or `String`). Enums with a raw type get conformance automatically. Use `init?(rawValue:)` to create, `.rawValue` to extract.",
        'ex': """enum Suit: String, CaseIterable { case hearts, diamonds, clubs, spades }

print(Suit.hearts.rawValue) // "hearts"
if let s = Suit(rawValue: "clubs") { print(s) } // clubs"""
    },
    'repeat': {
        'def': "The loop-introducer in `repeat-while` — Swift's do-while. The body runs once, then the condition is checked; if true, the body runs again. Unlike `while`, the body always runs at least once.",
        'ex': """var n = 0
repeat {
    print(n)
    n += 1
} while n < 3
// 0
// 1
// 2"""
    },
    'required': {
        'def': "A modifier on a class initializer that forces every subclass to implement it (unless the subclass also satisfies it via inheritance). Use it to ensure every subclass provides a particular way of being constructed.",
        'ex': """class Shape {
    required init() { print("shape") }
}

class Circle: Shape {
    required init() { super.init(); print("circle") }
}

let c = Circle()
// shape
// circle"""
    },
    'Result': {
        'def': "A standard-library enum with two cases — `.success(value)` and `.failure(error)` — that represents an operation's outcome as a value. Prefer `async throws` for new code; `Result` still shines for callback-based APIs or when passing results across threads.",
        'ex': """func divide(_ a: Int, by b: Int) -> Result<Int, Error> {
    guard b != 0 else {
        return .failure(NSError(domain: "math", code: 1))
    }
    return .success(a / b)
}

switch divide(10, by: 0) {
case .success(let v): print(v)
case .failure(let e): print("error: \\(e)")
}"""
    },
    'rethrows': {
        'def': "A function modifier that says \"this function only throws if the closure the caller passed in throws.\" Standard-library higher-order functions like `map` and `filter` use `rethrows` so non-throwing calls don't force the caller into a `do/catch`.",
        'ex': """func tryTwice<T>(_ body: () throws -> T) rethrows -> T {
    do { return try body() }
    catch { return try body() }
}

// Non-throwing closure — caller doesn't need try/catch:
let x = tryTwice { 42 }

// Throwing closure — caller must handle:
// try tryTwice { try someThrowingCall() }"""
    },
    'return': {
        'def': "Exits the current function or method, optionally handing back a value. In single-expression functions, `return` is implicit and can be omitted.",
        'ex': """func square(_ n: Int) -> Int {
    return n * n
}

// Equivalent single-expression form:
func cube(_ n: Int) -> Int { n * n * n }

print(square(3)) // 9
print(cube(3))   // 27"""
    },
    '@resultBuilder': {
        'def': "An attribute on a type whose static methods (`buildBlock`, `buildOptional`, `buildEither`, etc.) teach the compiler how to compose values in a declarative, structure-preserving way. The mechanism powers SwiftUI's `some View`, regex builder, and custom DSLs.",
        'ex': """@resultBuilder
struct StringBuilder {
    static func buildBlock(_ parts: String...) -> String {
        parts.joined(separator: "\\n")
    }
}

@StringBuilder
func haiku() -> String {
    "old pond"
    "a frog leaps in"
    "splash"
}

print(haiku())"""
    },

    # ---------- S ----------
    'Self': {
        'def': "The type of the current enclosing type — capital-S. Useful in protocol requirements and in generic code where \"return an instance of whatever type I'm called on\" matters.",
        'ex': """protocol Clonable {
    func clone() -> Self
}

struct Item: Clonable {
    var name: String
    func clone() -> Item { self } // Self here means Item
}"""
    },
    'self': {
        'def': "The current instance within a method (lowercase-s). You only need to write it when disambiguating from a parameter of the same name or capturing in a closure.",
        'ex': """struct Player {
    var score: Int
    mutating func add(_ score: Int) {
        self.score += score // self disambiguates from parameter
    }
}

var p = Player(score: 10)
p.add(5)
print(p.score) // 15"""
    },
    'Sendable': {
        'def': "A marker protocol for types safe to share across actor / task boundaries — they have no internal mutable state that races. Value types of Sendable members are automatically Sendable; classes have to prove it (`final`, immutable, or `@unchecked`).",
        'ex': """struct Coord: Sendable { let x, y: Int }

actor Tracker {
    func remember(_ c: Coord) { /* safe: Coord is Sendable */ }
}

let t = Tracker()
Task { await t.remember(Coord(x: 1, y: 2)) }"""
    },
    'Sequence': {
        'def': "The most abstract protocol for things you can iterate once. A `Sequence` has a `makeIterator()` and yields elements. `Collection` refines it with the ability to iterate multiple times and index.",
        'ex': """struct Countdown: Sequence, IteratorProtocol {
    var n: Int
    mutating func next() -> Int? {
        guard n > 0 else { return nil }
        defer { n -= 1 }
        return n
    }
}

for x in Countdown(n: 3) { print(x) }
// 3
// 2
// 1"""
    },
    'Set': {
        'def': "An unordered collection of unique `Hashable` values. Lookups, inserts, and membership tests are O(1) on average. Use Set when order doesn't matter and uniqueness does.",
        'ex': """var tags: Set<String> = ["swift", "ios"]
tags.insert("macos")
tags.insert("swift") // duplicate — ignored
print(tags.count)    // 3
print(tags.contains("ios")) // true"""
    },
    'some': {
        'def': "Marks an opaque type — the function returns \"some specific type conforming to the given protocol, but the caller doesn't get to know which type.\" The concrete type is fixed per call site; SwiftUI's `some View` is the standard example.",
        'ex': """protocol Shape { func area() -> Double }
struct Square: Shape { let side: Double; func area() -> Double { side * side } }

func unitShape() -> some Shape {
    Square(side: 1)
}

let s = unitShape()
print(s.area()) // 1.0"""
    },
    'static': {
        'def': "Makes a member belong to the type itself, not to instances. Useful for factory methods, constants, and utility functions. On classes, `static` is non-overridable; use `class` if you want subclasses to override.",
        'ex': """struct Temperature {
    let celsius: Double
    static let freezing = Temperature(celsius: 0)
    static func fromFahrenheit(_ f: Double) -> Temperature {
        Temperature(celsius: (f - 32) * 5 / 9)
    }
}

print(Temperature.freezing.celsius)            // 0.0
print(Temperature.fromFahrenheit(212).celsius) // 100.0"""
    },
    'String': {
        'def': "A Unicode-correct, value-typed string. Iterating a `String` yields `Character` values (which may each be composed of multiple Unicode scalars). String literals use double quotes; multi-line literals use triple quotes.",
        'ex': """let name = "Ada"
let greeting = "Hello, \\(name)!"
print(greeting) // Hello, Ada!

let multi = \"\"\"
    line one
    line two
\"\"\"

print(name.count) // 3"""
    },
    'struct': {
        'def': "A value type — when you assign or pass a struct, you make a copy (with copy-on-write under the hood for standard-library collections). Structs can conform to protocols, have methods, and participate in generics; they don't support inheritance.",
        'ex': """struct Point {
    var x: Double, y: Double
    func distance(to other: Point) -> Double {
        let dx = other.x - x, dy = other.y - y
        return (dx*dx + dy*dy).squareRoot()
    }
}

let a = Point(x: 0, y: 0)
var b = a
b.x = 3
print(a.x, b.x) // 0.0 3.0 — independent copies"""
    },
    'subscript': {
        'def': "A special method that lets a type be indexed with `[…]` syntax. Subscripts can take multiple parameters, be read-only or read-write, and be generic.",
        'ex': """struct Board {
    var cells: [[Int]]
    subscript(row: Int, col: Int) -> Int {
        get { cells[row][col] }
        set { cells[row][col] = newValue }
    }
}

var b = Board(cells: [[1,2],[3,4]])
print(b[0, 1]) // 2
b[1, 1] = 99
print(b.cells)"""
    },
    'super': {
        'def': "Refers to the superclass from within a subclass. Use `super.method()` to call the overridden version, and `super.init(...)` to delegate to a superclass initializer.",
        'ex': """class Animal {
    func speak() { print("...") }
}
class Dog: Animal {
    override func speak() {
        super.speak()
        print("woof")
    }
}

Dog().speak()
// ...
// woof"""
    },
    'switch': {
        'def': "A multi-way control-flow statement that matches a value against patterns. Swift's switch is exhaustive — every possible value must be handled (use `default` or `@unknown default` for catch-alls). Patterns can include tuples, ranges, `where` clauses, and value bindings.",
        'ex': """let point = (x: 0, y: 5)
switch point {
case (0, 0): print("origin")
case (_, 0): print("on x-axis")
case (0, _): print("on y-axis")
case let (x, y) where x == y: print("diagonal")
default: print("elsewhere")
}
// on y-axis"""
    },
    '@State': {
        'def': "A SwiftUI property wrapper that owns a piece of transient view-local state. Writes trigger the view to re-render. Use `@State` only inside views and only for types the view fully owns.",
        'ex': """struct Counter: View {
    @State private var n = 0
    var body: some View {
        Button("tap \\(n)") { n += 1 }
    }
}"""
    },
    '@StateObject': {
        'def': "A SwiftUI property wrapper that creates and owns an `ObservableObject` for the lifetime of the view. Use it when the VIEW creates the object; use `@ObservedObject` when the object is handed in from outside.",
        'ex': """final class Model: ObservableObject {
    @Published var items: [String] = []
}

struct Root: View {
    @StateObject private var model = Model()
    var body: some View {
        Button("add") { model.items.append("\\(model.items.count)") }
    }
}"""
    },
    '@SceneStorage': {
        'def': "A SwiftUI property wrapper that persists a value per scene — so each window / screen keeps its own copy across backgrounding and relaunch. Supports the same value types as `@AppStorage`.",
        'ex': """struct DraftNote: View {
    @SceneStorage("draft") private var draft = ""
    var body: some View {
        TextField("note", text: $draft)
    }
}"""
    },
    '@Sendable': {
        'def': "An attribute on a closure parameter declaring the closure must be `Sendable` — safe to hand across actor and task boundaries. The compiler then checks that any captures are themselves `Sendable`.",
        'ex': """func dispatch(_ work: @Sendable @escaping () -> Void) {
    Task.detached { work() }
}

dispatch { print("ran on another task") }"""
    },
    '#selector': {
        'def': "A compile-time-checked selector expression for Objective-C interop. The method it names must be `@objc`. Prefer modern Swift APIs; `#selector` is still needed for `Timer`, some `Notification` APIs, and gesture recognizers via UIKit bridging.",
        'ex': """import Foundation

class Alarm: NSObject {
    @objc func ring() { print("rrring") }
}

let a = Alarm()
_ = #selector(Alarm.ring) // compile-checked"""
    },

    # ---------- T ----------
    'Task': {
        'def': "A unit of asynchronous work. `Task { ... }` runs the block on a task separate from the current one; the task has a priority, a cancellation flag, and produces a `Task<Value, Error>` handle you can `await`.",
        'ex': """let t = Task {
    try await Task.sleep(nanoseconds: 100_000_000)
    return "done"
}

Task {
    let v = try await t.value
    print(v) // done
}"""
    },
    'TaskGroup': {
        'def': "Runs multiple child tasks in parallel and yields their results as they finish. Child tasks added to the group are automatically awaited before the group returns, and cancelling the group cancels its children.",
        'ex': """func fetch(_ id: Int) async -> Int { id * 2 }

let results = await withTaskGroup(of: Int.self) { group -> [Int] in
    for id in 1...3 { group.addTask { await fetch(id) } }
    var out: [Int] = []
    for await value in group { out.append(value) }
    return out
}
print(results.sorted()) // [2, 4, 6]"""
    },
    'throw': {
        'def': "Raises an error from inside a function declared `throws` (or `rethrows` with a throwing closure). Control flow leaves the current scope and passes up until a `do/catch` handles it.",
        'ex': """enum InputError: Error { case empty }

func first(_ s: String) throws -> Character {
    guard let c = s.first else { throw InputError.empty }
    return c
}

do { print(try first("hi")) } // h
catch { print("error: \\(error)") }"""
    },
    'throws': {
        'def': "A modifier on a function declaration saying the function may throw an error. Callers must use `try` (or `try?` / `try!`) and handle or propagate the error.",
        'ex': """func parse(_ s: String) throws -> Int {
    guard let n = Int(s) else {
        throw NSError(domain: "parse", code: 1)
    }
    return n
}

let n = try? parse("42") // Optional(42)
let bad = try? parse("nope") // nil"""
    },
    'true': {
        'def': "One of the two `Bool` literal values, representing logical truth. The other is `false`.",
        'ex': """let isReady: Bool = true
if isReady { print("go") }"""
    },
    'try': {
        'def': "Marks a call site where the called function may throw. Flavors: `try` inside a `do/catch` propagates the error to `catch`, `try?` converts to an Optional (nil on throw), and `try!` traps if the call throws.",
        'ex': """func mayThrow() throws -> Int { 42 }

do { print(try mayThrow()) }
catch { print(error) }

let opt = try? mayThrow()  // Optional(42)
let forced = try! mayThrow() // 42, or crash"""
    },
    'typealias': {
        'def': "Introduces a new name for an existing type — useful for shortening long generic types, documenting intent, or making signatures read more naturally.",
        'ex': """typealias Meters = Double
typealias Handler = (Result<Data, Error>) -> Void

let distance: Meters = 1500

func fetch(_ done: Handler) { /* ... */ }"""
    },
    '@testable': {
        'def': "An attribute on `import`, written `@testable import MyModule`, that exposes the module's `internal` declarations to the importing (test) module. Use only in test targets.",
        'ex': """// In MyAppTests/SomeTests.swift:
@testable import MyApp

final class MyTests: XCTestCase {
    func testInternalThing() {
        // Can call internal helpers of MyApp here.
    }
}"""
    },

    # ---------- U ----------
    'unowned': {
        'def': "A capture or property modifier for a class reference that doesn't bump the reference count and doesn't become Optional. Use it when the referenced object is guaranteed to outlive the reference; accessing it after deinit traps.",
        'ex': """class Owner {
    var child: Child?
}
class Child {
    unowned let parent: Owner
    init(parent: Owner) { self.parent = parent }
}

let o = Owner()
let c = Child(parent: o)
o.child = c"""
    },
    '@UIApplicationMain': {
        'def': "A legacy attribute on a UIKit `UIApplicationDelegate` that marks it as the app's entry point. Superseded by `@main` + `UIApplicationDelegateAdaptor` in SwiftUI lifecycles; still seen in UIKit-only apps.",
        'ex': """import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ app: UIApplication,
                     didFinishLaunchingWithOptions opts: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        true
    }
}"""
    },

    # ---------- V ----------
    'var': {
        'def': "Declares a mutable binding — you can reassign the variable and (for value types) mutate through it. Use `let` by default and promote to `var` only when you need mutation.",
        'ex': """var count = 0
count += 1
print(count) // 1

var numbers = [1, 2, 3]
numbers.append(4)
print(numbers) // [1, 2, 3, 4]"""
    },
    'Void': {
        'def': "A typealias for the empty tuple `()`. A function that returns `Void` returns nothing meaningful; writing `-> Void` is optional since it's the default return type.",
        'ex': """func log(_ s: String) -> Void { print(s) }

// Equivalent:
func log2(_ s: String) { print(s) }

let callback: () -> Void = { print("done") }
callback()"""
    },

    # ---------- X ----------
    'XMLParser': {
        'def': "A Foundation class that reads XML by streaming events (start-element, characters, end-element) to a delegate. Lower-level than `JSONDecoder` — you walk the tree yourself — but the standard way to read XML on Apple platforms. Use a third-party library (e.g. `XMLCoder`) for Codable-style XML.",
        'ex': """import Foundation

final class Handler: NSObject, XMLParserDelegate {
    var titles: [String] = []
    private var inTitle = false
    func parser(_ p: XMLParser, didStartElement name: String,
                namespaceURI: String?, qualifiedName qName: String?,
                attributes: [String: String] = [:]) {
        inTitle = (name == \"title\")
    }
    func parser(_ p: XMLParser, foundCharacters s: String) {
        if inTitle { titles.append(s) }
    }
}

let xml = \"\"\"<feed><title>Hi</title><title>There</title></feed>\"\"\"
    .data(using: .utf8)!
let p = XMLParser(data: xml)
let h = Handler(); p.delegate = h
p.parse()
print(h.titles) // [\"Hi\", \"There\"]"""
    },

    # ---------- Z ----------
    'ZStack': {
        'def': "A SwiftUI container that lays out its children on top of each other along the Z-axis — the one pointing out of the screen. The first child renders at the back, the last at the front. Use for overlays, badges, and stacked images.",
        'ex': """import SwiftUI

struct Avatar: View {
    var body: some View {
        ZStack(alignment: .bottomTrailing) {
            Circle()
                .fill(.blue)
                .frame(width: 80, height: 80)
            Image(systemName: \"checkmark.seal.fill\")
                .foregroundStyle(.green)
                .background(Circle().fill(.white))
        }
    }
}"""
    },

    # ---------- W ----------
    'weak': {
        'def': "A capture or property modifier for a class reference that doesn't bump the reference count and becomes `nil` automatically when the referenced object is deallocated. Always Optional. Use it to break retain cycles.",
        'ex': """class Parent {
    var child: Child?
}
class Child {
    weak var parent: Parent?
}

let p = Parent()
let c = Child()
c.parent = p
p.child = c // no cycle: parent is weak"""
    },
    'where': {
        'def': "Adds a constraint. On a generic parameter, it narrows allowed types. On a `case`, `for`, or `switch`, it adds a pattern guard. On a protocol extension, it restricts when the extension applies.",
        'ex': """extension Collection where Element: Numeric {
    func total() -> Element {
        reduce(.zero, +)
    }
}

print([1, 2, 3].total()) // 6

for n in 1...10 where n.isMultiple(of: 3) {
    print(n)
}"""
    },
    'while': {
        'def': "Runs its body repeatedly as long as the condition stays true. The condition is checked before every iteration, so the body may run zero times. Contrast with `repeat-while`, which always runs at least once.",
        'ex': """var n = 10
while n > 0 {
    print(n)
    n -= 2
}
// 10 8 6 4 2"""
    },
    '#warning': {
        'def': "Emits a compile-time warning with the given message. Useful as a breadcrumb for work-in-progress code so you can't ship without noticing.",
        'ex': """func placeholder() -> Int {
    #warning("TODO: implement real calculation")
    return 0
}"""
    },
}
