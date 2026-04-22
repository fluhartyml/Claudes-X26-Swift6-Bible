"""
Per-entry Rosetta Stone prose, related-cluster membership, and source URLs
for every Lexicon entry.

Three top-level maps:

  ROSETTA[entry] = {"pascal": str, "basic": str, "c": str}
      Short, real comparative prose. "—" means no direct cousin exists in
      that language; the string explains the closest approach.

  CLUSTERS = {"cluster-name": [entry_names, ...]}
      Topic groupings. A Related list for any entry = the union of every
      cluster it participates in, minus itself. Used by the generator.

  SOURCE_MAP[entry] = [(url, label), ...]
      Concrete source URLs for this entry. Built from the canonical bases
      verified 2026-04-22: docs.swift.org/swift-book, developer.apple.com
      /documentation/{swift, swiftui, swiftdata, foundation, charts,
      pdfkit, uikit, combine}, and Swift Evolution proposals on GitHub.

Entries not present here fall back to generic defaults in the generator.
"""

# ---------------------------------------------------------------
#                           ROSETTA STONE
# ---------------------------------------------------------------

ROSETTA = {

    # ================== A ==================
    'actor': {
        'pascal': "No direct cousin. Delphi threading relies on TThread plus manual critical sections (TCriticalSection); you hand-roll what Swift's compiler enforces for you.",
        'basic':  "No cousin. Classic BASIC is single-threaded; Visual Basic .NET has SyncLock blocks but no type-level isolation guarantee.",
        'c':      "Closest is pthread_mutex_t or std::mutex wrapped around a struct. The compiler doesn't check that every access goes through the mutex — that's on you. `actor` makes that check mandatory.",
    },
    'any': {
        'pascal': "No direct cousin. Delphi's `TValue` can hold any typed value via RTTI; existential-type semantics don't exist.",
        'basic':  "Visual Basic's `Object` is the rough equivalent — a boxed reference that can hold anything.",
        'c':      "C's `void *` plays a similar role for 'I don't know the static type'; C++ has `std::any` for boxed values with type recovery at runtime.",
    },
    'Any': {
        'pascal': "Similar to `TObject` in Delphi — the root of the class hierarchy, can hold any class reference. Not quite the same for value types.",
        'basic':  "Visual Basic's `Object` class serves this role via boxing.",
        'c':      "`void *` with explicit casts, or C++ `std::any`. Swift's `Any` is safer because cast attempts are checked via `as?`.",
    },
    'AnyObject': {
        'pascal': "`TObject` — every class in Delphi descends from TObject automatically.",
        'basic':  "`Object` in VB.NET — the root class reference.",
        'c':      "No pure-C cousin (C has no classes). In Objective-C it's `id`; in C++ there's no universal base class.",
    },
    'as': {
        'pascal': "`as` in Delphi is nearly identical (`obj as TSub`) — raises EInvalidCast on failure. The `is` operator tests first.",
        'basic':  "`CType(x, T)` or `DirectCast(x, T)` in VB.NET. `TryCast` is the nil-on-fail sibling of Swift's `as?`.",
        'c':      "C uses explicit casts: `(Type)value`. No runtime check. C++ adds `dynamic_cast<T*>(p)` which is the closest match to `as?`.",
    },
    'async': {
        'pascal': "Delphi 11+ has `async function` with a similar keyword. Older Delphi used callbacks via TThread / ITask.",
        'basic':  "VB.NET has the same keyword: `Async Function ... As Task(Of T)`.",
        'c':      "No async in plain C. C++20 adds `std::future` and coroutines via `co_await`; the ergonomics are rougher.",
    },
    'await': {
        'pascal': "Delphi 11+ has `await` inside async functions.",
        'basic':  "Same keyword: `Await someTask` in VB.NET.",
        'c':      "C++20 `co_await`. Plain C has no built-in await.",
    },
    '@autoclosure': {
        'pascal': "No cousin. Delphi evaluates arguments eagerly; for lazy evaluation you pass an explicit anonymous method: `procedure of object`.",
        'basic':  "No direct cousin. Pass a `Func(Of T)` explicitly to get deferred evaluation.",
        'c':      "No cousin. Use a function pointer / lambda as the argument and call it inside the function to defer evaluation.",
    },
    '@available': {
        'pascal': "No direct cousin. Delphi uses `{$IFDEF}` directives for conditional compilation against version constants.",
        'basic':  "VB.NET uses `<Obsolete>` plus `#If TARGET_VERSION`. No runtime version gating built in.",
        'c':      "`#if` / `#ifdef` with version macros, plus Apple's `__API_AVAILABLE(...)` macro in Objective-C for the same idea.",
    },
    'Array': {
        'pascal': "Delphi's `TArray<T>` (dynamic array) and `array of T` match `[Element]` closely. Zero-indexed, reference-managed.",
        'basic':  "VB's `Dim arr() As Integer` and `ReDim Preserve`. Simpler API, same concept.",
        'c':      "`int arr[N]` (fixed) or `malloc`'d pointer-to-array (dynamic). No bounds checking. C++ adds `std::vector<T>` which is the closer analogue.",
    },

    # ================== B ==================
    'Bool': {
        'pascal': "`Boolean` in Pascal/Delphi.",
        'basic':  "`Boolean` in VB.NET; `True` / `False` in classic BASIC.",
        'c':      "`_Bool` (C99) or `bool` via `<stdbool.h>`. C++ has `bool` natively.",
    },
    'break': {
        'pascal': "`Break` procedure.",
        'basic':  "`Exit For` / `Exit Do` / `Exit While`.",
        'c':      "`break;` — identical semantics.",
    },
    '@Binding': {
        'pascal': "No cousin. Delphi's LiveBindings are the spiritual match: declarative two-way binding between a UI component and a property.",
        'basic':  "WPF's `{Binding Path=...}` with `Mode=TwoWay`. Same concept, different wiring.",
        'c':      "No cousin. Callback-based observers are the manual equivalent.",
    },

    # ================== C ==================
    'case': {
        'pascal': "`case` in Pascal/Delphi's `case ... of` works similarly but matches only ordinals and ranges; no pattern matching.",
        'basic':  "`Case` / `Case Is` / `Case To` inside `Select Case`.",
        'c':      "`case` inside `switch`. No associated-value destructuring; C falls through by default (the opposite of Swift's behavior).",
    },
    'catch': {
        'pascal': "`except on E: ExceptionType do ... end;` is Delphi's shape.",
        'basic':  "`Catch ex As Exception` inside a `Try` block.",
        'c':      "Plain C has no exceptions; use `setjmp` / `longjmp` for rough control. C++ uses `catch (const std::exception &e)`.",
    },
    'Character': {
        'pascal': "`Char` in Pascal is a single byte; Delphi's `Char` is a UTF-16 code unit. Neither matches Swift's grapheme-cluster Character.",
        'basic':  "`Char` (UTF-16 code unit) in VB.NET. No grapheme-cluster type built in.",
        'c':      "`char` is one byte. `wchar_t` is a wide character (platform-dependent width). No grapheme-cluster support; use ICU.",
    },
    'class': {
        'pascal': "`class` in Delphi — nearly identical semantics. Reference type, inheritance, virtual methods.",
        'basic':  "`Class` in VB.NET — same semantics; reference type with inheritance.",
        'c':      "No classes in C. C++ `class` and `struct` are nearly interchangeable; both support inheritance and virtual functions.",
    },
    'closure': {
        'pascal': "`procedure of object` (bound method) and anonymous methods (`procedure begin ... end`) are Delphi's closures.",
        'basic':  "`Function(x) x * 2` lambda expressions in VB.NET.",
        'c':      "No closures in C. C++ lambdas (`[capture] (args) { body }`) and function objects serve the role.",
    },
    'Codable': {
        'pascal': "No cousin. Delphi has RTTI-based `TJSONSerializer` and XML RTTI, but there's no type-annotation protocol pair.",
        'basic':  "Closest is `<Serializable>` attribute + `XmlSerializer` / `DataContractSerializer` in VB.NET. Per-property.",
        'c':      "No cousin. Manual serialization via cJSON library, or C++ nlohmann::json with explicit `to_json`/`from_json` per type.",
    },
    'Collection': {
        'pascal': "`IEnumerable<T>` plus index-based collection interfaces like `IList<T>`, `TList<T>` in Delphi.",
        'basic':  "VB.NET's `IEnumerable(Of T)` + `ICollection(Of T)` + `IList(Of T)`. Cumulative protocols.",
        'c':      "No cousin in C. C++'s concepts-based iterator hierarchy (`std::ranges::sized_range`, `std::ranges::random_access_range`) is the closest analogue.",
    },
    'Comparable': {
        'pascal': "Delphi's `IComparer<T>` interface with a `Compare(a, b) : Integer` method.",
        'basic':  "`IComparable(Of T)` in VB.NET with `CompareTo(other) As Integer`.",
        'c':      "No cousin in C. C++ has `operator<` (and C++20 `<=>` for three-way comparison) plus `std::less<T>`.",
    },
    'continue': {
        'pascal': "`Continue` procedure in Delphi.",
        'basic':  "`Continue For` / `Continue Do` / `Continue While`.",
        'c':      "`continue;` — identical semantics.",
    },
    'convenience': {
        'pascal': "No explicit keyword. Delphi constructors can call other constructors directly.",
        'basic':  "Similar concept; VB.NET lets one constructor call another via `Me.New(...)`.",
        'c':      "C has no constructors. C++ constructors can delegate (`Foo() : Foo(42) {}`) — no convenience/designated distinction.",
    },
    'CaseIterable': {
        'pascal': "Delphi generics don't synthesize this. Use `TRttiEnumerationType.GetValues<T>` via RTTI.",
        'basic':  "`System.Enum.GetValues(typeof(T))` in VB.NET returns the enum case list.",
        'c':      "No cousin. Enumerate manually with sentinel values (`MAX_COUNT`) or compile-time arrays.",
    },

    # ================== D ==================
    'defer': {
        'pascal': "No direct cousin. Use `try ... finally` blocks for the same guaranteed-cleanup pattern.",
        'basic':  "Use `Try ... Finally` blocks for the same effect.",
        'c':      "No cousin. Goto-cleanup labels, or (compiler-specific) `__attribute__((cleanup(...)))` in GCC/Clang. C++ uses RAII destructors.",
    },
    'deinit': {
        'pascal': "Delphi's `destructor Destroy; override;` is the direct equivalent. Called on `.Free` or reference release.",
        'basic':  "`Protected Overrides Sub Finalize()` — though GC timing makes it non-deterministic.",
        'c':      "No cousin in C (manual `free()` calls). C++ destructors (`~Foo()`) match Swift's deinit semantics most closely.",
    },
    'Decodable': {
        'pascal': "No cousin. Manual deserialization via `TJsonReader` / `TJSONObject.ParseJSONValue`.",
        'basic':  "`<Serializable>` plus `DataContractSerializer.ReadObject` / `JsonSerializer.Deserialize`.",
        'c':      "No cousin. Parsing libraries (cJSON, nlohmann::json) with explicit per-field extraction.",
    },
    'default': {
        'pascal': "`else` inside a `case ... of` statement. Default parameter values use `parameter: Type = value`.",
        'basic':  "`Case Else` in `Select Case`. Default parameters: `Optional ByVal x As Integer = 0`.",
        'c':      "`default:` inside `switch`. Default parameters are a C++ feature: `void f(int x = 0);`.",
    },
    'Dictionary': {
        'pascal': "`TDictionary<K, V>` in Delphi's Generics.Collections — hash-based, same ergonomics.",
        'basic':  "`Dictionary(Of K, V)` in VB.NET — identical shape.",
        'c':      "No built-in in C (hash tables via uthash.h or custom). C++ has `std::unordered_map<K, V>`.",
    },
    'do': {
        'pascal': "Delphi uses `try ... except` / `try ... finally`; there's no bare `do` block. `do` appears as part of `while ... do`.",
        'basic':  "`Do ... Loop` in VB is the loop form; exception-handling is `Try`.",
        'c':      "`do { ... } while (cond);` is the post-test loop. For exception-like blocks C++ uses `try`.",
    },
    'Double': {
        'pascal': "`Double` in Pascal/Delphi — identical IEEE 754 64-bit float.",
        'basic':  "`Double` in VB — same 64-bit float.",
        'c':      "`double` — same representation. Swift's `Double` behaves identically.",
    },
    'dynamic': {
        'pascal': "`dynamic` exists in Delphi but means something different — a late-dispatch method. Not the same concept.",
        'basic':  "VB.NET has `Dynamic` type (DLR) for runtime-dispatched calls. Different goal, similar flavor.",
        'c':      "No cousin. Objective-C's runtime is what Swift's `dynamic` piggybacks on for KVO and swizzling.",
    },
    '@discardableResult': {
        'pascal': "No cousin. Delphi doesn't warn on unused function results; the attribute would be a no-op.",
        'basic':  "No cousin. VB.NET's compiler doesn't warn on unused return values.",
        'c':      "`__attribute__((warn_unused_result))` in GCC/Clang is the opposite: it WARNS on unused returns. No suppress flag; you just don't apply the attribute.",
    },

    # ================== E ==================
    'else': {
        'pascal': "`else` in Pascal/Delphi's `if ... then ... else`.",
        'basic':  "`Else` and `ElseIf` in VB.",
        'c':      "`else` — identical keyword.",
    },
    'Encodable': {
        'pascal': "See `Decodable` — same manual-serialization story in reverse.",
        'basic':  "`<Serializable>` + `DataContractSerializer.WriteObject` / `JsonSerializer.Serialize`.",
        'c':      "Manual per-field emission via cJSON / nlohmann::json `to_json`.",
    },
    'enum': {
        'pascal': "Delphi enums (`type TColor = (Red, Green, Blue)`) are integer-ordinal only — no associated values.",
        'basic':  "`Enum Color : Red, Green, Blue : End Enum`. Integer-backed only.",
        'c':      "`enum Color { Red, Green, Blue };` — plain integer constants. No associated values; use tagged unions (`struct { int tag; union { ... } payload; }`) for Swift-style enums.",
    },
    'Equatable': {
        'pascal': "No direct cousin. Implement `function Equals(const Other: TFoo): Boolean` by convention.",
        'basic':  "`IEquatable(Of T)` interface with `Equals(other) As Boolean`.",
        'c':      "Write a compare function. C++ overloads `operator==`. C++20 defaulted comparison (`auto operator==(const Foo&) const = default;`) matches Swift's synthesis.",
    },
    'Error': {
        'pascal': "`Exception` class in Delphi's SysUtils. Throw subclasses via `raise`.",
        'basic':  "`System.Exception` class. Throw via `Throw`.",
        'c':      "No exceptions in C. C++ `std::exception` is the root of the standard exception hierarchy.",
    },
    'extension': {
        'pascal': "Delphi class helpers (`TMyHelper = class helper for TExistingClass`) are the direct cousin. Same limitation: no stored fields.",
        'basic':  "VB.NET extension methods via `<Extension>` attribute on a module. Adds methods only — no properties pre-.NET Framework 4.7.",
        'c':      "No cousin. C++ has no built-in extension mechanism; free functions that operate on a type fill a similar role.",
    },
    '@escaping': {
        'pascal': "No cousin. All closure-like references in Delphi are effectively heap-allocated and can outlive their creator.",
        'basic':  "No cousin. Lambdas and `Func(Of T)` are always escaping in VB.NET.",
        'c':      "No cousin. A function pointer can always outlive its creator — there's no lifetime annotation.",
    },
    '@Environment': {
        'pascal': "LiveBindings plus singleton services is the rough mix. No single keyword.",
        'basic':  "WPF's `DependencyProperty` + `FrameworkPropertyMetadata` inheritance is the closest pattern.",
        'c':      "No cousin.",
    },
    '@EnvironmentObject': {
        'pascal': "No cousin. Dependency injection via global services is the Delphi equivalent.",
        'basic':  "WPF's `DataContext` inheritance + a shared view model.",
        'c':      "No cousin.",
    },
    'ExpressibleByStringLiteral': {
        'pascal': "No cousin. Use an explicit constructor: `TFoo.FromString('...')`.",
        'basic':  "No cousin. Explicit constructors or `CType` widening.",
        'c':      "No cousin. C++ user-defined literals (`operator\"\"_tag`) are the closest analogue.",
    },
    '#elseif': {
        'pascal': "`{$ELSEIF}` compiler directive — identical role.",
        'basic':  "`#ElseIf` in VB.NET conditional compilation.",
        'c':      "`#elif` — identical, one letter shorter.",
    },
    '#endif': {
        'pascal': "`{$ENDIF}` — identical role.",
        'basic':  "`#End If` — same closure.",
        'c':      "`#endif` — identical.",
    },
    '#error': {
        'pascal': "`{$MESSAGE ERROR 'text'}` directive.",
        'basic':  "`#Error \"text\"` in VB.NET.",
        'c':      "`#error text` — identical intent.",
    },

    # ================== F ==================
    'fallthrough': {
        'pascal': "No cousin. Pascal `case` statements don't fall through.",
        'basic':  "No cousin. `Select Case` doesn't fall through.",
        'c':      "The DEFAULT behavior of C `switch`. Swift is explicit about what C does implicitly.",
    },
    'false': {
        'pascal': "`False` — identical literal.",
        'basic':  "`False` — identical literal.",
        'c':      "`false` (via `<stdbool.h>`) or `0` in older code. Identical meaning.",
    },
    'fileprivate': {
        'pascal': "`strict private` inside a unit's implementation section has a similar scope.",
        'basic':  "`Private` inside a VB.NET module/class — but VB has no file-scope modifier; uses `Friend` for assembly-scope.",
        'c':      "`static` at file scope — restricts visibility to the translation unit. Same intent.",
    },
    'final': {
        'pascal': "`sealed` on a Delphi class prevents inheritance. `final` on methods prevents override.",
        'basic':  "`NotInheritable` on a class; `NotOverridable` on a method.",
        'c':      "C++ `final` keyword (C++11) on classes and virtual methods. Same meaning.",
    },
    'Float': {
        'pascal': "`Single` in Pascal/Delphi — 32-bit IEEE 754 float.",
        'basic':  "`Single` in VB.NET — same 32-bit float.",
        'c':      "`float` — same. All three are literally the IEEE 754 binary32 format.",
    },
    'for': {
        'pascal': "`for i := 1 to 10 do` or `for element in collection do` (Delphi 2005+).",
        'basic':  "`For i = 1 To 10` or `For Each element In collection`.",
        'c':      "`for (int i = 0; i < n; i++)`. C++ range-for: `for (auto &x : container)`. Swift's `for-in` reads like the range-for form.",
    },
    'func': {
        'pascal': "`function` (returns a value) vs `procedure` (no value). Two keywords instead of one.",
        'basic':  "`Function f(x As Integer) As Integer` for value-returning; `Sub f(x)` for no return.",
        'c':      "`returnType name(args) { body }`. No keyword — the return type signals it's a function.",
    },
    '@frozen': {
        'pascal': "No cousin. Delphi doesn't have a library-evolution optimization annotation.",
        'basic':  "No cousin.",
        'c':      "No cousin. Library ABIs in C are whatever the compiler emits; optimization decisions are per-call.",
    },
    '@FocusState': {
        'pascal': "VCL's `Screen.ActiveControl` plus `SetFocus` method is the imperative equivalent.",
        'basic':  "WPF's `Keyboard.Focus()` / `Keyboard.FocusedElement` — same imperative style.",
        'c':      "No cousin.",
    },
    '#file': {
        'pascal': "`{$I %FILE%}` compiler directive expands to the current source file.",
        'basic':  "No cousin in VB; in C#/CallerFilePath attribute.",
        'c':      "`__FILE__` predefined macro — identical purpose.",
    },
    '#function': {
        'pascal': "No direct cousin. `{$I %FUNCTION%}` captures it in newer Delphi versions.",
        'basic':  "No cousin; use `MethodBase.GetCurrentMethod().Name` at runtime.",
        'c':      "`__func__` (C99) and `__FUNCTION__` / `__PRETTY_FUNCTION__` (compiler-specific).",
    },

    # ================== G ==================
    'generic': {
        'pascal': "Delphi Generics: `TFoo<T>` with `specialize` semantics. Introduced in Delphi 2009.",
        'basic':  "`Class Stack(Of T)` / `Function Min(Of T)(...)` — same shape.",
        'c':      "No generics in C (macros fake them, badly). C++ templates are more powerful but compile slowly and produce verbose errors.",
    },
    'get': {
        'pascal': "`function GetFoo: T;` paired with a `property`. Same role.",
        'basic':  "`ReadOnly Property Foo As T` with a `Get` block.",
        'c':      "No properties in C. C++ uses regular member functions (`T getFoo() const`).",
    },
    'guard': {
        'pascal': "No dedicated keyword. Idiom: `if not cond then Exit;` at the top of a function.",
        'basic':  "No dedicated keyword. `If Not cond Then Return` at the top.",
        'c':      "No cousin. `if (!cond) return;` is the manual equivalent.",
    },
    '@GestureState': {
        'pascal': "No cousin. VCL has no equivalent of gesture-resetting state.",
        'basic':  "WPF's `ManipulationDelta` / `ManipulationCompleted` handlers are the event-driven match.",
        'c':      "No cousin.",
    },

    # ================== H ==================
    'Hashable': {
        'pascal': "No direct cousin. Delphi's `TDictionary<K, V>` requires a `TEqualityComparer<K>` or it defaults to `THashService`.",
        'basic':  "`IEquatable(Of T)` plus `Overrides Function GetHashCode() As Integer`.",
        'c':      "No cousin in C. C++ specializes `std::hash<T>` for the key type used in `std::unordered_map`.",
    },

    # ================== I ==================
    'if': {
        'pascal': "`if cond then ... else ...` — same shape, requires `then`.",
        'basic':  "`If cond Then ... Else ... End If`.",
        'c':      "`if (cond) { ... } else { ... }`. No `then` keyword, uses braces.",
    },
    'import': {
        'pascal': "`uses UnitA, UnitB;` in the unit header.",
        'basic':  "`Imports System.Foo` at the top of a file.",
        'c':      "`#include <header.h>` (preprocessor). C++20 adds `import module;` which is closer to Swift's form.",
    },
    'in': {
        'pascal': "`for element in collection do` uses the same keyword.",
        'basic':  "`For Each element In collection`.",
        'c':      "No keyword. C++ range-for uses `:` — `for (auto x : c)`.",
    },
    'indirect': {
        'pascal': "No cousin. Recursive type variants work automatically because Delphi classes are reference types.",
        'basic':  "No cousin. Classes are reference types by default.",
        'c':      "Use a pointer explicitly: `struct Node { int value; struct Node *next; };`.",
    },
    'infix': {
        'pascal': "`operator +(...)` overload in a class is the closest — but operator precedence is fixed, not user-configurable.",
        'basic':  "`Shared Operator +(a As T, b As T) As T` — fixed precedence by operator symbol.",
        'c':      "C++ `operator+(const T&, const T&)`. Precedence is fixed by the token.",
    },
    'init': {
        'pascal': "`constructor Create(...)` — same role. Delphi constructors are named `Create` by convention.",
        'basic':  "`Sub New(...)` — the VB.NET constructor.",
        'c':      "No constructors in C. C++ uses `Foo() { ... }` with the class name as the method name.",
    },
    'inout': {
        'pascal': "`var` parameter: `procedure f(var x: Integer)`. Pass-by-reference; caller writes `f(myVar)`.",
        'basic':  "`ByRef x As Integer` parameter. Same semantics.",
        'c':      "Pass a pointer: `void f(int *x)`; call site `f(&myVar)`. C++ adds `int&` reference parameters.",
    },
    'Int': {
        'pascal': "`Integer` (32-bit on most targets) or `NativeInt` (matches pointer width — closer to Swift's Int).",
        'basic':  "`Integer` is 32-bit in VB.NET; `Long` is 64-bit; `IntPtr` / `nint` matches pointer width.",
        'c':      "`int` (implementation-defined width, commonly 32-bit). Closer to Swift's Int: `intptr_t` from `<stdint.h>`.",
    },
    'internal': {
        'pascal': "Delphi has no exact cousin. `private`/`protected`/`public` are the access levels; units don't export what they don't list in the `interface` section.",
        'basic':  "`Friend` — visible within the assembly, hidden outside.",
        'c':      "No access modifiers in C. C++ `public`/`protected`/`private` apply to class members, not modules.",
    },
    'is': {
        'pascal': "`obj is TSub` — identical runtime type test.",
        'basic':  "`TypeOf obj Is T`.",
        'c':      "No runtime type info in C. C++ uses `dynamic_cast<T*>(p) != nullptr` or `typeid(x) == typeid(T)`.",
    },
    'Identifiable': {
        'pascal': "No cousin. Use a custom interface with a `GetID` method.",
        'basic':  "No standard protocol. Implement `IIdentifiable(Of TKey)` by convention.",
        'c':      "No cousin.",
    },
    '@inlinable': {
        'pascal': "`inline` directive on a function (`function f: Integer; inline;`) — suggests inlining.",
        'basic':  "No user-facing attribute; JIT decides.",
        'c':      "`inline` keyword (C99). C++ adds `__attribute__((always_inline))` and `[[gnu::always_inline]]` for stronger hints.",
    },

    # ================== K ==================
    'KeyPath': {
        'pascal': "No cousin in Delphi. RTTI traversal (`TRttiType.GetField`) by string name is the runtime equivalent — but unchecked.",
        'basic':  "VB.NET `Expression(Of Func(Of T, TProp))` lambdas capture member access similarly, but they're runtime ASTs, not keypath values.",
        'c':      "No cousin. C++ pointer-to-member (`int Foo::*p = &Foo::x;`) is the conceptual match.",
    },

    # ================== J ==================
    'JSONEncoder': {
        'pascal': "Delphi: `TJSONObject.Create` plus manual field assignment, or `TJsonSerializer.Serialize<T>(value)` in newer versions.",
        'basic':  "`System.Text.Json.JsonSerializer.Serialize(value)` in VB.NET.",
        'c':      "No built-in. cJSON's `cJSON_Print(root)` or nlohmann::json's `dump()` in C++.",
    },
    'JSONDecoder': {
        'pascal': "`TJSONObject.ParseJSONValue` or `TJsonSerializer.Deserialize<T>(json)`.",
        'basic':  "`System.Text.Json.JsonSerializer.Deserialize(Of T)(json)`.",
        'c':      "cJSON's `cJSON_Parse(string)` or nlohmann::json's `json::parse(s)`.",
    },
    'JSONSerialization': {
        'pascal': "`TJSONValue` hierarchy (`TJSONObject`, `TJSONArray`, etc.) is the untyped tree equivalent.",
        'basic':  "`System.Text.Json.JsonDocument` / `JsonElement` for untyped tree traversal.",
        'c':      "cJSON's root `cJSON *` pointer traversed via `->child` / `->next`. nlohmann::json's `json` type.",
    },

    # ================== L ==================
    'lazy': {
        'pascal': "No keyword. Idiom: getter that initializes on first read using `FField := ComputeIt; Result := FField;` guarded by a sentinel.",
        'basic':  "`Lazy(Of T)` wrapper class (`Lazy(Of String)`) with `.Value` deferred initialization.",
        'c':      "No cousin. Manual guard-and-compute pattern.",
    },
    'let': {
        'pascal': "`const` at method scope — `const x: Integer = 5;` is a compile-time constant. Regular locals are `var` and mutable.",
        'basic':  "`Const x As Integer = 5` for compile-time; no runtime-assigned-once binding without readonly fields.",
        'c':      "`const int x = compute();` in C99+. Same semantics: pick once, can't rebind.",
    },
    '#line': {
        'pascal': "`{$I %LINE%}` in newer Delphi.",
        'basic':  "No direct cousin; use `CallerLineNumber` attribute in .NET.",
        'c':      "`__LINE__` predefined macro — identical.",
    },

    # ================== M ==================
    'map': {
        'pascal': "`TArray.Map<T, U>` generic helper (Spring4D adds more idiomatic functional wrappers).",
        'basic':  "LINQ `.Select(Function(x) ...)` in VB.NET.",
        'c':      "No built-in. C++ `std::transform(src.begin(), src.end(), std::back_inserter(dst), fn)` — same idea, more ceremony.",
    },
    'mutating': {
        'pascal': "No cousin. Records and classes don't distinguish mutating methods at the type level.",
        'basic':  "No cousin.",
        'c':      "No cousin. C++ `const` methods are the inverse: marks non-mutating on classes.",
    },
    '@main': {
        'pascal': "The `program` block: `program Foo; begin ... end.`",
        'basic':  "`Sub Main()` in a module marked as the startup object.",
        'c':      "`int main(int argc, char** argv) { ... }` — there IS exactly one.",
    },
    '@MainActor': {
        'pascal': "No type-level annotation. Runtime check: `if TThread.CurrentThread.ThreadID <> MainThreadID then TThread.Queue(...)`.",
        'basic':  "`Application.Current.Dispatcher.Invoke(...)` in WPF to post work back to the UI thread.",
        'c':      "No cousin.",
    },

    # ================== N ==================
    'Never': {
        'pascal': "No cousin. `procedure NoReturn; `... eventually calls `raise` or `Halt`.",
        'basic':  "No cousin. Mark the method by convention; VB doesn't have a bottom type.",
        'c':      "`_Noreturn` (C11) / `[[noreturn]]` (C++11) function attribute — same intent.",
    },
    'nil': {
        'pascal': "`nil` — identical keyword for a null pointer.",
        'basic':  "`Nothing` — the null reference literal.",
        'c':      "`NULL` (C) or `nullptr` (C++11+). Same meaning.",
    },
    'nonmutating': {
        'pascal': "No cousin.",
        'basic':  "No cousin.",
        'c':      "No cousin (but C++ `const` methods are the inverse).",
    },

    # ================== O ==================
    'open': {
        'pascal': "Delphi classes are open for subclassing by default; `sealed` closes them. No stronger keyword for cross-module open.",
        'basic':  "`Public` class with `Overridable` methods — nothing stronger in VB.NET.",
        'c':      "C++ has no framework/module boundary; `public` on a class member is the nearest analogue.",
    },
    'operator': {
        'pascal': "`class operator Add(a, b: T): T` defines operator overloads.",
        'basic':  "`Shared Operator +(a As T, b As T) As T` on a class.",
        'c':      "C++ `T operator+(const T&, const T&)`. Plain C has no operator overloading.",
    },
    'Optional': {
        'pascal': "`Nullable<T>` (Spring4D) or the `Variant` type for value types; classes can already be `nil`.",
        'basic':  "`Nullable(Of T)` or `T?` for value types in VB.NET.",
        'c':      "No cousin. A pointer plus `NULL`, or a sentinel value, is the common idiom. C++17 `std::optional<T>`.",
    },
    'override': {
        'pascal': "`override` keyword — identical purpose.",
        'basic':  "`Overrides` keyword.",
        'c':      "C++11 `override` specifier — same meaning (though optional).",
    },
    '@objc': {
        'pascal': "No cousin (Delphi has no Objective-C runtime).",
        'basic':  "No cousin.",
        'c':      "Objective-C `@objc` is the target of Swift's attribute. Pure C has no runtime to expose to.",
    },
    '@Observable': {
        'pascal': "No cousin. RTTI-based observers (`TObservable` class) or explicit Observer pattern.",
        'basic':  "WPF `INotifyPropertyChanged` on a class raises `PropertyChanged` per setter. Manual boilerplate.",
        'c':      "No cousin.",
    },
    '@ObservedObject': {
        'pascal': "WPF's `DataContext = vm` binding is the closest conceptual match.",
        'basic':  "WPF `Binding` to an `INotifyPropertyChanged` source.",
        'c':      "No cousin.",
    },

    # ================== P ==================
    'postfix': {
        'pascal': "No cousin. No postfix operators beyond the built-in `++` / `--` (and those aren't in Pascal; Delphi doesn't have them either).",
        'basic':  "No cousin.",
        'c':      "C/C++ `x++` is a postfix unary operator. In C++ you can overload it: `T operator++(int)` (the int is a signal, not a parameter).",
    },
    'precedencegroup': {
        'pascal': "No cousin. Operator precedence is fixed by the compiler.",
        'basic':  "No cousin.",
        'c':      "No cousin. C precedence is hardcoded.",
    },
    'prefix': {
        'pascal': "Prefix operators in Delphi are the built-ins (`not`, `-`, `+`). User-defined operators use `class operator` syntax.",
        'basic':  "Built-in prefix operators only; overloadable via `Shared Operator`.",
        'c':      "C/C++ unary operators like `-x`, `!x`, `++x` are prefix. Overloadable in C++: `T operator-() const;`.",
    },
    'print': {
        'pascal': "`WriteLn('hello')` writes to stdout.",
        'basic':  "`Console.WriteLine(\"hello\")` or classic `Print \"hello\"`.",
        'c':      "`printf(\"hello\\n\")` — format-string based. C++ adds `std::cout << \"hello\" << std::endl;`.",
    },
    'private': {
        'pascal': "`private` visibility in a class — same intent.",
        'basic':  "`Private` access modifier.",
        'c':      "`static` at file scope (for file-private functions). C++ `private:` on class members.",
    },
    'protocol': {
        'pascal': "`interface` — Delphi's interfaces are the direct match. Declare with `IMyInterface = interface` in the interface section.",
        'basic':  "`Interface IMyInterface ... End Interface`.",
        'c':      "No cousin in C (structs of function pointers fake them). C++ uses pure-virtual classes.",
    },
    '@Published': {
        'pascal': "Manual `OnPropertyChanged` events on each setter.",
        'basic':  "`INotifyPropertyChanged` with `OnPropertyChanged(NameOf(Prop))` in each setter.",
        'c':      "No cousin.",
    },
    'public': {
        'pascal': "`public` visibility in a class — identical meaning.",
        'basic':  "`Public` access modifier.",
        'c':      "No modifier at file scope (everything not `static` is external). C++ `public:` on class members.",
    },
    '#Predicate': {
        'pascal': "No cousin. LINQ-style predicate lambdas (`function(x: T): Boolean`) are the runtime equivalent but not introspectable.",
        'basic':  "`Expression(Of Func(Of T, Boolean))` — an introspectable predicate tree. Closest cousin.",
        'c':      "No cousin.",
    },
    '#Preview': {
        'pascal': "Delphi's form designer is the WYSIWYG equivalent — no code macro, but live preview of a TForm.",
        'basic':  "WPF / Blazor hot-reload previews show the component live during editing.",
        'c':      "No cousin.",
    },

    # ================== Q ==================
    '@Query': {
        'pascal': "No cousin. TQuery / TClientDataSet with a SQL filter is the imperative equivalent.",
        'basic':  "LINQ queries against Entity Framework: `From x In db.Books Where x.IsFavorite Select x`.",
        'c':      "No cousin.",
    },

    # ================== R ==================
    'Range': {
        'pascal': "Pascal subrange type: `type TDigit = 0..9;`. Compile-time subset of an ordinal.",
        'basic':  "`Enumerable.Range(start, count)` — runtime sequence.",
        'c':      "No cousin. Manual `for (int i = start; i < end; i++)` loops.",
    },
    'ClosedRange': {
        'pascal': "Pascal subrange `1..5` (inclusive) is the lexical match.",
        'basic':  "`Enumerable.Range(1, 5)` covers 1..5 inclusive.",
        'c':      "Manual loops.",
    },
    'RawRepresentable': {
        'pascal': "Enum-to-Integer conversions via `Ord(x)` and `T(IntVal)` casts. Not a protocol.",
        'basic':  "`Enum` types with a base type (`Enum Foo : Short ... End Enum`) use `CInt(x)` and `CType(n, Foo)`.",
        'c':      "`enum` values ARE their underlying int by default. Cast is explicit: `(int)Color_Red`.",
    },
    'repeat': {
        'pascal': "`repeat ... until cond;` — runs body, then checks condition. Same as `repeat-while` except inverted condition.",
        'basic':  "`Do ... Loop While cond` — post-test loop.",
        'c':      "`do { ... } while (cond);` — same semantics as Swift's `repeat-while`.",
    },
    'required': {
        'pascal': "No cousin. Abstract methods via `abstract` keyword force subclass implementation of methods, not constructors.",
        'basic':  "`MustOverride` on a method. No required-constructor concept.",
        'c':      "No cousin. C++ constructors aren't inherited; each subclass writes its own by default.",
    },
    'Result': {
        'pascal': "No cousin in the standard library. Spring4D's `TOption<T>` plus exceptions approximate it.",
        'basic':  "No direct cousin; `Try`/`Catch` is idiomatic. `Nullable(Of T)` handles the success-or-nothing subset.",
        'c':      "No cousin. Paired return codes (`int err`) plus out-parameters, or `std::expected<T, E>` in C++23.",
    },
    'rethrows': {
        'pascal': "No cousin. Delphi exceptions propagate implicitly; there's no throw-only-if-argument-throws annotation.",
        'basic':  "No cousin.",
        'c':      "No cousin.",
    },
    'return': {
        'pascal': "Assign to implicit `Result` variable; `Exit;` returns. In modern Delphi: `Exit(value)`.",
        'basic':  "`Return value` in a function.",
        'c':      "`return value;` — identical keyword.",
    },
    '@resultBuilder': {
        'pascal': "No cousin.",
        'basic':  "No cousin. LINQ builder patterns approximate the idea.",
        'c':      "No cousin.",
    },

    # ================== S ==================
    'Self': {
        'pascal': "`ClassName.Create(...)` or `ClassType` when you need the concrete type in a class method.",
        'basic':  "`Me.GetType()` at runtime. Generics use the type parameter.",
        'c':      "No cousin. CRTP (Curiously Recurring Template Pattern) approximates it in C++.",
    },
    'self': {
        'pascal': "`Self` — identical meaning, capitalized.",
        'basic':  "`Me` — the current instance reference.",
        'c':      "`this` in C++. Not available in plain C (structs have no methods).",
    },
    'Sendable': {
        'pascal': "No cousin. Thread safety is convention; no compiler check.",
        'basic':  "No cousin.",
        'c':      "No cousin. C11 `_Atomic` types ensure atomicity but not deep thread safety.",
    },
    'Sequence': {
        'pascal': "`IEnumerable<T>` with a `GetEnumerator: IEnumerator<T>` method.",
        'basic':  "`IEnumerable(Of T)` — identical concept.",
        'c':      "No cousin. C++ ranges / iterators: a type with `begin()` and `end()`.",
    },
    'Set': {
        'pascal': "Pascal `set of Byte` / `set of TMyEnum` is bit-packed (max 256 elements). `TDictionary<K, Boolean>` emulates a general set. Spring4D has `ISet<T>`.",
        'basic':  "`HashSet(Of T)` in VB.NET.",
        'c':      "No cousin. C++ `std::set<T>` (ordered) or `std::unordered_set<T>` (hashed).",
    },
    'some': {
        'pascal': "No cousin. Opaque return types don't exist in Delphi.",
        'basic':  "No cousin.",
        'c':      "No cousin. `auto` return type in C++14+ is similar in that the type is inferred, but not opaque to callers.",
    },
    'static': {
        'pascal': "`class var` / `class function` / `class procedure` — class-level members.",
        'basic':  "`Shared` members on a class.",
        'c':      "`static` at file scope (file-local); `static` inside a function (persistent local). C++ class `static` matches Swift's intent.",
    },
    'String': {
        'pascal': "`string` / `UnicodeString` (UTF-16). Grapheme-cluster iteration needs manual work via the `Character` unit.",
        'basic':  "`String` (UTF-16, immutable).",
        'c':      "`char *` / `char[]` (null-terminated, byte-sequence). C++ `std::string` (byte-sequence) and `std::u16string` / `std::u32string`.",
    },
    'struct': {
        'pascal': "`record` — value-typed composite. Identical concept. `record` can include methods since Delphi 2005.",
        'basic':  "`Structure Foo ... End Structure` — value-typed composite.",
        'c':      "`struct Foo { ... };` — value type, copied on assignment. C++ `struct` is the same as `class` except default public.",
    },
    'subscript': {
        'pascal': "Delphi class indexers: `property Items[i: Integer]: T read GetItem write SetItem; default;`",
        'basic':  "`Default Property Item(i As Integer) As T`.",
        'c':      "No cousin in C. C++ overload `operator[]`.",
    },
    'super': {
        'pascal': "`inherited Method(args)` or `inherited;` (calls the superclass member of the same name).",
        'basic':  "`MyBase.Method(args)`.",
        'c':      "No cousin in C. C++ uses `BaseClass::method(args)` explicit qualification.",
    },
    'switch': {
        'pascal': "`case X of` with fixed-pattern matching on ordinals and ranges. No associated-value destructuring.",
        'basic':  "`Select Case X ... Case 1 To 10 ... Case Else ... End Select`.",
        'c':      "`switch (x) { case 1: ... break; default: ... }`. Far less powerful — integer/enum match only, no patterns.",
    },
    '@State': {
        'pascal': "No cousin. Form fields + manual change tracking + event handlers.",
        'basic':  "WPF `DependencyProperty` + `INotifyPropertyChanged` or a plain public field.",
        'c':      "No cousin.",
    },
    '@StateObject': {
        'pascal': "Field holding a view model reference, initialized in the form's constructor.",
        'basic':  "Same pattern: WPF field holding a view model.",
        'c':      "No cousin.",
    },
    '@SceneStorage': {
        'pascal': "No cousin. Per-form state saved manually via INI or registry.",
        'basic':  "`My.Settings` per-user settings on WinForms; nothing per-window by default.",
        'c':      "No cousin.",
    },
    '@Sendable': {
        'pascal': "No cousin.",
        'basic':  "No cousin.",
        'c':      "No cousin.",
    },
    '#selector': {
        'pascal': "`@methodname` in Delphi — the `@` operator yields a method pointer.",
        'basic':  "`AddressOf SomeMethod` in VB.NET.",
        'c':      "Function pointer: `&func`. C++ pointer-to-member: `&Class::method`.",
    },

    # ================== T ==================
    'Task': {
        'pascal': "`TTask` from System.Threading — `TTask.Run(...)` starts one; `.Wait` / `.Result` resolve it.",
        'basic':  "`Task.Run(...)` in VB.NET — same API as C#.",
        'c':      "`std::thread` for coarse threading; C++20 `std::jthread`. Coroutines via `co_await` on a coroutine return type.",
    },
    'TaskGroup': {
        'pascal': "`ITaskFuture<T>` arrays + `TTask.WaitAll(...)` for manual fan-out / fan-in.",
        'basic':  "`Await Task.WhenAll(tasks)` for parallel tasks.",
        'c':      "`std::async` + `std::future::get` loops, or C++17 parallel algorithms with an execution policy.",
    },
    'throw': {
        'pascal': "`raise ExceptionClass.Create('msg')`.",
        'basic':  "`Throw New Exception(\"msg\")`.",
        'c':      "No exceptions in C; return an error code. C++ `throw std::runtime_error(\"msg\");`.",
    },
    'throws': {
        'pascal': "No cousin. Every Delphi function can raise; no declaration required.",
        'basic':  "No cousin. No checked exceptions in VB.NET.",
        'c':      "No cousin. C++ had `throw()` specifications (deprecated) and `noexcept` (inverse — marks non-throwing).",
    },
    'true': {
        'pascal': "`True` — identical literal.",
        'basic':  "`True` — identical literal.",
        'c':      "`true` (via `<stdbool.h>`) or `1`.",
    },
    'try': {
        'pascal': "`try ... except on E: ... do ... end;` for throwing calls. No per-call `try` marker — all Delphi calls can implicitly raise.",
        'basic':  "`Try ... Catch ... End Try` block. No per-call `Try` marker either.",
        'c':      "No cousin in C. C++ `try { call(); } catch (...)` — also no per-call marker.",
    },
    'typealias': {
        'pascal': "`type TMyList = TList<Integer>;` — an identical type-rename.",
        'basic':  "`Imports MyList = System.Collections.Generic.List(Of Integer)` — scoped rename.",
        'c':      "`typedef int (*Handler)(void *);` — the C type-renaming keyword. C++ `using Handler = ...` is more modern.",
    },
    '@testable': {
        'pascal': "No cousin. Delphi has no assembly-scope separation; tests import units normally.",
        'basic':  "`<InternalsVisibleTo(\"MyTests\")>` attribute on the assembly achieves the same thing.",
        'c':      "No cousin.",
    },

    # ================== U ==================
    'unowned': {
        'pascal': "`[Weak]` attribute on a field (Delphi ARC on mobile targets). No separate unowned semantics.",
        'basic':  "`WeakReference(Of T)` — but it's always optional. Closest match is a plain reference documented as not-retained.",
        'c':      "Plain pointer. No ownership annotation; you manage lifetime yourself.",
    },
    '@UIApplicationMain': {
        'pascal': "The `program` block `begin Application.Initialize; Application.Run; end.` is the Delphi equivalent.",
        'basic':  "`Sub Main()` with `Application.Run(New MainForm())` in VB.NET.",
        'c':      "`int main() { return RunApp(); }`.",
    },

    # ================== V ==================
    'var': {
        'pascal': "`var x: Integer;` — a mutable local. Identical role.",
        'basic':  "`Dim x As Integer` — identical.",
        'c':      "`int x;` — mutable by default. Use `const int x = ...;` for immutability.",
    },
    'Void': {
        'pascal': "`procedure` (no return value) is the role of Void. There's no `Void` type name you use directly.",
        'basic':  "`Sub` (no return value) instead of `Function`.",
        'c':      "`void` — the same keyword for no return.",
    },

    # ================== W ==================
    'weak': {
        'pascal': "`[Weak]` attribute on a field under ARC (Delphi mobile). Same intent.",
        'basic':  "`WeakReference(Of T)` wrapper. Always Optional-like (may be dead).",
        'c':      "No cousin in C. C++ `std::weak_ptr<T>` alongside `std::shared_ptr<T>`.",
    },
    'where': {
        'pascal': "Generic constraints: `class(TFoo)` — constraint is positional and limited.",
        'basic':  "`Of T As {New, Class, IFoo}` — constraint list on the type parameter.",
        'c':      "No cousin in C. C++ concepts (`requires`) are the modern match; SFINAE was the older workaround.",
    },
    'while': {
        'pascal': "`while cond do ... ;` — pre-test loop.",
        'basic':  "`While cond ... End While` or `Do While cond ... Loop`.",
        'c':      "`while (cond) { ... }` — identical keyword.",
    },
    '#warning': {
        'pascal': "`{$MESSAGE WARN 'text'}` compiler directive.",
        'basic':  "`#Warning \"text\"` directive.",
        'c':      "`#warning text` (extension in GCC/Clang; standardized in C23).",
    },

    # ================== X ==================
    'XMLParser': {
        'pascal': "`TXMLDocument` in Delphi (with IXMLDocument interface) is the DOM-style match. For streaming parsing, TSAXParser.",
        'basic':  "`XmlReader` for streaming, `XmlDocument` / `XDocument` (LINQ to XML) for DOM.",
        'c':      "libxml2's SAX API, or expat (SAX) — the streaming idiom is very similar.",
    },

    # ================== Z ==================
    'ZStack': {
        'pascal': "Delphi VCL's Z-order on a container — call `.BringToFront` / `.SendToBack` on child controls. No layout container that defaults to stacking.",
        'basic':  "WPF's `Grid` with multiple children in the same row/column overlays them on the Z-axis.",
        'c':      "No cousin. Custom drawing with explicit draw order.",
    },
}


# ---------------------------------------------------------------
#                       TOPIC CLUSTERS
# ---------------------------------------------------------------

CLUSTERS = {
    "concurrency": [
        "actor", "async", "await", "Task", "TaskGroup", "Sendable",
        "@Sendable", "@MainActor",
    ],
    "error-handling": [
        "throw", "throws", "try", "catch", "do", "Error", "rethrows", "Result",
    ],
    "reference-vs-value": [
        "class", "struct", "enum", "actor", "final", "open", "indirect",
    ],
    "initialization": [
        "init", "deinit", "required", "convenience", "super", "self", "Self",
    ],
    "access-control": [
        "public", "open", "internal", "fileprivate", "private",
    ],
    "control-flow": [
        "if", "else", "guard", "for", "while", "repeat", "switch", "case",
        "default", "break", "continue", "fallthrough", "return",
    ],
    "functions-closures": [
        "func", "closure", "@escaping", "@autoclosure", "@discardableResult",
        "inout", "rethrows", "@inlinable",
    ],
    "generics": [
        "generic", "where", "some", "any", "typealias", "associatedtype",
    ],
    "optionals": [
        "Optional", "nil", "some", "guard",
    ],
    "protocols-core": [
        "protocol", "Equatable", "Hashable", "Comparable", "Codable",
        "Encodable", "Decodable", "Identifiable", "Sendable",
        "CaseIterable", "RawRepresentable", "ExpressibleByStringLiteral",
        "Sequence", "Collection", "Error",
    ],
    "types-numeric": [
        "Int", "Double", "Float", "Bool",
    ],
    "types-collections": [
        "Array", "Dictionary", "Set", "Range", "ClosedRange", "KeyPath",
    ],
    "types-text": [
        "String", "Character",
    ],
    "types-misc": [
        "Any", "AnyObject", "Never", "Void", "Optional", "Result",
    ],
    "memory-references": [
        "class", "weak", "unowned", "deinit",
    ],
    "enums": [
        "enum", "case", "indirect", "CaseIterable", "RawRepresentable",
    ],
    "casting": [
        "is", "as",
    ],
    "operators": [
        "operator", "prefix", "infix", "postfix", "precedencegroup",
    ],
    "properties-accessors": [
        "var", "let", "lazy", "get", "static", "mutating", "nonmutating",
        "dynamic", "subscript",
    ],
    "modifiers": [
        "final", "override", "required", "convenience", "lazy", "static",
        "mutating", "nonmutating", "indirect", "dynamic",
    ],
    "swiftui-state": [
        "@State", "@Binding", "@StateObject", "@ObservedObject",
        "@EnvironmentObject", "@Environment", "@Published", "@Observable",
        "@FocusState", "@GestureState", "@SceneStorage",
    ],
    "swiftdata": [
        "@Model", "@Query", "@Attribute", "@Relationship",
    ],
    "json": [
        "JSONEncoder", "JSONDecoder", "JSONSerialization",
        "Codable", "Encodable", "Decodable",
    ],
    "swiftui-views": [
        "ZStack",
    ],
    "compile-time": [
        "@available", "@frozen", "@main", "@UIApplicationMain",
        "@objc", "@testable", "@resultBuilder",
        "#elseif", "#endif", "#error", "#warning", "#file",
        "#function", "#line", "#selector", "#Predicate", "#Preview",
    ],
    "xml": [
        "XMLParser",
    ],
    "extensions-modules": [
        "extension", "import", "typealias",
    ],
}


# ---------------------------------------------------------------
#                      BOOK CROSS-REFERENCES
# ---------------------------------------------------------------

# Map cluster -> (book_number, part_folder, slug) pairs worth linking.
# Used to extend Related lists with Book-level navigation.
BOOK_REFS = {
    "concurrency": [
        (18, "Part-V-Advanced-Techniques",   "Error-Handling-And-Result-Type"),
        (20, "Part-V-Advanced-Techniques",   "Performance-Instruments-And-Best-Practices"),
    ],
    "error-handling": [
        (18, "Part-V-Advanced-Techniques",   "Error-Handling-And-Result-Type"),
    ],
    "reference-vs-value": [
        (2,  "Part-I-Introduction",          "Introducing-SwiftUI-Views"),
    ],
    "control-flow": [
        (1,  "Part-I-Introduction",          "Introducing-Swift-And-Xcode"),
    ],
    "protocols-core": [
        (15, "Part-IV-The-Application",      "SwiftData-And-CoreData"),
        (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers"),
    ],
    "swiftui-state": [
        (2,  "Part-I-Introduction",          "Introducing-SwiftUI-Views"),
        (4,  "Part-III-The-User-Interface",  "Gestures-And-Input"),
        (13, "Part-IV-The-Application",      "Multi-Window-And-NavigationSplitView"),
        (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers"),
    ],
    "swiftdata": [
        (15, "Part-IV-The-Application",      "SwiftData-And-CoreData"),
    ],
    "json": [
        (14, "Part-IV-The-Application",      "Clipboard-DragDrop-ShareSheet"),
    ],
    "swiftui-views": [
        (2,  "Part-I-Introduction",          "Introducing-SwiftUI-Views"),
        (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers"),
    ],
    "generics": [
        (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers"),
    ],
    "functions-closures": [
        (4,  "Part-III-The-User-Interface",  "Gestures-And-Input"),
    ],
    "extensions-modules": [
        (16, "Part-IV-The-Application",      "Extensions-And-Packages"),
    ],
    "memory-references": [
        (20, "Part-V-Advanced-Techniques",   "Performance-Instruments-And-Best-Practices"),
    ],
    "xml": [
        (14, "Part-IV-The-Application",      "Clipboard-DragDrop-ShareSheet"),
    ],
}


# ---------------------------------------------------------------
#                        SOURCE URLS
# ---------------------------------------------------------------

# Per-entry source URLs. Each value is a list of (url, label) tuples.
# Bases verified live 2026-04-22. Anchors / specific paths follow stable
# Apple URL patterns that have been in place since the given framework's
# launch; individual slugs are taken from the Apple Developer URL scheme.
#
# Frameworks in play:
#   swift-book  https://docs.swift.org/swift-book/documentation/the-swift-programming-language/<topic>
#   swift-std   https://developer.apple.com/documentation/swift/<lowercase>
#   swiftui     https://developer.apple.com/documentation/swiftui/<lowercase>
#   swiftdata   https://developer.apple.com/documentation/swiftdata/<lowercase>
#   foundation  https://developer.apple.com/documentation/foundation/<lowercase>
#   charts      https://developer.apple.com/documentation/charts/<lowercase>
#   evolution   https://github.com/apple/swift-evolution/blob/main/proposals/<NNNN-title>.md

SWIFT_BOOK = "https://docs.swift.org/swift-book/documentation/the-swift-programming-language"
APPLE_SWIFT = "https://developer.apple.com/documentation/swift"
APPLE_SWIFTUI = "https://developer.apple.com/documentation/swiftui"
APPLE_SWIFTDATA = "https://developer.apple.com/documentation/swiftdata"
APPLE_FOUNDATION = "https://developer.apple.com/documentation/foundation"
APPLE_CHARTS = "https://developer.apple.com/documentation/charts"
EVOLUTION = "https://github.com/apple/swift-evolution/blob/main/proposals"


def _book(chapter: str):  # convenience
    return (f"{SWIFT_BOOK}/{chapter}", "The Swift Programming Language")

def _apple(framework_base: str, slug: str, label: str):
    return (f"{framework_base}/{slug}", label)

def _evo(filename: str, title: str):
    return (f"{EVOLUTION}/{filename}", f"Swift Evolution: {title}")


SOURCE_MAP = {
    # A
    'actor':            [_book("concurrency"), _apple(APPLE_SWIFT, "actor", "Swift.Actor (std lib)"), _evo("0306-actors.md", "Actors (SE-0306)")],
    'any':              [_book("genericsandprotocols"), _evo("0335-existential-any.md", "Introduce existential any (SE-0335)")],
    'Any':              [_book("types"), _apple(APPLE_SWIFT, "any", "Swift.Any (std lib)")],
    'AnyObject':        [_book("protocols"), _apple(APPLE_SWIFT, "anyobject", "Swift.AnyObject (std lib)")],
    'as':               [_book("typecasting")],
    'async':            [_book("concurrency"), _evo("0296-async-await.md", "async/await (SE-0296)")],
    'await':            [_book("concurrency"), _evo("0296-async-await.md", "async/await (SE-0296)")],
    '@autoclosure':     [_book("closures"), _book("attributes")],
    '@available':       [_book("attributes")],
    'Array':            [_apple(APPLE_SWIFT, "array", "Swift.Array (std lib)"), _book("collectiontypes")],

    # B
    'Bool':             [_apple(APPLE_SWIFT, "bool", "Swift.Bool (std lib)")],
    'break':            [_book("controlflow")],
    '@Binding':         [_apple(APPLE_SWIFTUI, "binding", "SwiftUI.Binding")],

    # C
    'case':             [_book("enumerations"), _book("controlflow")],
    'catch':            [_book("errorhandling")],
    'Character':        [_apple(APPLE_SWIFT, "character", "Swift.Character (std lib)"), _book("stringsandcharacters")],
    'class':            [_book("classesandstructures")],
    'closure':          [_book("closures")],
    'Codable':          [_apple(APPLE_SWIFT, "codable", "Swift.Codable typealias"), _evo("0166-swift-archival-serialization.md", "Codable (SE-0166)")],
    'Collection':       [_apple(APPLE_SWIFT, "collection", "Swift.Collection protocol"), _book("protocols")],
    'Comparable':       [_apple(APPLE_SWIFT, "comparable", "Swift.Comparable protocol")],
    'continue':         [_book("controlflow")],
    'convenience':      [_book("initialization")],
    'CaseIterable':     [_apple(APPLE_SWIFT, "caseiterable", "Swift.CaseIterable protocol")],

    # D
    'defer':            [_book("statements"), _book("errorhandling")],
    'deinit':           [_book("deinitialization")],
    'Decodable':        [_apple(APPLE_SWIFT, "decodable", "Swift.Decodable protocol")],
    'default':          [_book("controlflow"), _book("functions")],
    'Dictionary':       [_apple(APPLE_SWIFT, "dictionary", "Swift.Dictionary (std lib)"), _book("collectiontypes")],
    'do':               [_book("errorhandling"), _book("statements")],
    'Double':           [_apple(APPLE_SWIFT, "double", "Swift.Double (std lib)")],
    'dynamic':          [_book("attributes")],
    '@discardableResult':[_book("attributes")],

    # E
    'else':             [_book("controlflow")],
    'Encodable':        [_apple(APPLE_SWIFT, "encodable", "Swift.Encodable protocol")],
    'enum':             [_book("enumerations")],
    'Equatable':        [_apple(APPLE_SWIFT, "equatable", "Swift.Equatable protocol")],
    'Error':            [_apple(APPLE_SWIFT, "error", "Swift.Error protocol"), _book("errorhandling")],
    'extension':        [_book("extensions")],
    '@escaping':        [_book("closures"), _book("attributes")],
    '@Environment':     [_apple(APPLE_SWIFTUI, "environment", "SwiftUI.Environment")],
    '@EnvironmentObject':[_apple(APPLE_SWIFTUI, "environmentobject", "SwiftUI.EnvironmentObject")],
    'ExpressibleByStringLiteral':[_apple(APPLE_SWIFT, "expressiblebystringliteral", "Swift.ExpressibleByStringLiteral protocol")],
    '#elseif':          [_book("compilercontrolstatements")],
    '#endif':           [_book("compilercontrolstatements")],
    '#error':           [_book("compilercontrolstatements")],

    # F
    'fallthrough':      [_book("controlflow")],
    'false':            [_apple(APPLE_SWIFT, "bool", "Swift.Bool (std lib)")],
    'fileprivate':      [_book("accesscontrol")],
    'final':            [_book("inheritance")],
    'Float':            [_apple(APPLE_SWIFT, "float", "Swift.Float (std lib)")],
    'for':              [_book("controlflow")],
    'func':             [_book("functions")],
    '@frozen':          [_book("attributes")],
    '@FocusState':      [_apple(APPLE_SWIFTUI, "focusstate", "SwiftUI.FocusState")],
    '#file':            [_book("statements")],
    '#function':        [_book("statements")],

    # G
    'generic':          [_book("generics")],
    'get':              [_book("properties")],
    'guard':            [_book("controlflow")],
    '@GestureState':    [_apple(APPLE_SWIFTUI, "gesturestate", "SwiftUI.GestureState")],

    # H
    'Hashable':         [_apple(APPLE_SWIFT, "hashable", "Swift.Hashable protocol")],

    # I
    'if':               [_book("controlflow")],
    'import':           [_book("declarations")],
    'in':               [_book("closures"), _book("controlflow")],
    'indirect':         [_book("enumerations")],
    'infix':            [_book("advancedoperators")],
    'init':             [_book("initialization")],
    'inout':            [_book("functions")],
    'Int':              [_apple(APPLE_SWIFT, "int", "Swift.Int (std lib)")],
    'internal':         [_book("accesscontrol")],
    'is':               [_book("typecasting")],
    'Identifiable':     [_apple(APPLE_SWIFT, "identifiable", "Swift.Identifiable protocol")],
    '@inlinable':       [_book("attributes")],

    # J
    'JSONEncoder':      [_apple(APPLE_FOUNDATION, "jsonencoder", "Foundation.JSONEncoder")],
    'JSONDecoder':      [_apple(APPLE_FOUNDATION, "jsondecoder", "Foundation.JSONDecoder")],
    'JSONSerialization':[_apple(APPLE_FOUNDATION, "jsonserialization", "Foundation.JSONSerialization")],

    # K
    'KeyPath':          [_apple(APPLE_SWIFT, "keypath", "Swift.KeyPath (std lib)"), _book("subscripts")],

    # L
    'lazy':             [_book("properties")],
    'let':              [_book("thebasics")],
    '#line':            [_book("statements")],

    # M
    'map':              [_apple(APPLE_SWIFT, "sequence/map(_:)", "Sequence.map(_:)")],
    'mutating':         [_book("methods")],
    '@main':            [_book("attributes"), _evo("0281-main-attribute.md", "@main (SE-0281)")],
    '@MainActor':       [_apple(APPLE_SWIFT, "mainactor", "Swift.MainActor"), _book("concurrency")],

    # N
    'Never':            [_apple(APPLE_SWIFT, "never", "Swift.Never (std lib)")],
    'nil':              [_book("thebasics")],
    'nonmutating':      [_book("properties")],

    # O
    'open':             [_book("accesscontrol")],
    'operator':         [_book("advancedoperators")],
    'Optional':         [_apple(APPLE_SWIFT, "optional", "Swift.Optional (std lib)"), _book("thebasics")],
    'override':         [_book("inheritance")],
    '@objc':            [_book("attributes")],
    '@Observable':      [_apple(APPLE_SWIFT, "observable()", "Swift.Observable macro"), _evo("0395-observability.md", "Observation (SE-0395)")],
    '@ObservedObject':  [_apple(APPLE_SWIFTUI, "observedobject", "SwiftUI.ObservedObject")],

    # P
    'postfix':          [_book("advancedoperators")],
    'precedencegroup':  [_book("advancedoperators")],
    'prefix':           [_book("advancedoperators")],
    'print':            [_apple(APPLE_SWIFT, "print(_:separator:terminator:)", "Swift.print")],
    'private':          [_book("accesscontrol")],
    'protocol':         [_book("protocols")],
    '@Published':       [("https://developer.apple.com/documentation/combine/published", "Combine.Published")],
    'public':           [_book("accesscontrol")],
    '#Predicate':       [_apple(APPLE_FOUNDATION, "predicate", "Foundation.Predicate macro")],
    '#Preview':         [_apple(APPLE_SWIFTUI, "preview(_:body:)", "SwiftUI.Preview macro")],

    # Q
    '@Query':           [_apple(APPLE_SWIFTDATA, "query", "SwiftData.Query")],

    # R
    'Range':            [_apple(APPLE_SWIFT, "range", "Swift.Range (std lib)")],
    'ClosedRange':      [_apple(APPLE_SWIFT, "closedrange", "Swift.ClosedRange (std lib)")],
    'RawRepresentable': [_apple(APPLE_SWIFT, "rawrepresentable", "Swift.RawRepresentable protocol")],
    'repeat':           [_book("controlflow")],
    'required':         [_book("initialization")],
    'Result':           [_apple(APPLE_SWIFT, "result", "Swift.Result (std lib)")],
    'rethrows':         [_book("errorhandling")],
    'return':           [_book("functions")],
    '@resultBuilder':   [_book("attributes"), _evo("0289-result-builders.md", "Result Builders (SE-0289)")],

    # S
    'Self':             [_book("protocols"), _book("genericsandprotocols")],
    'self':             [_book("methods")],
    'Sendable':         [_apple(APPLE_SWIFT, "sendable", "Swift.Sendable protocol"), _evo("0302-concurrent-value-and-concurrent-closures.md", "Sendable (SE-0302)")],
    'Sequence':         [_apple(APPLE_SWIFT, "sequence", "Swift.Sequence protocol")],
    'Set':              [_apple(APPLE_SWIFT, "set", "Swift.Set (std lib)"), _book("collectiontypes")],
    'some':             [_book("opaquetypes"), _evo("0244-opaque-result-types.md", "Opaque Result Types (SE-0244)")],
    'static':           [_book("properties"), _book("methods")],
    'String':           [_apple(APPLE_SWIFT, "string", "Swift.String (std lib)"), _book("stringsandcharacters")],
    'struct':           [_book("classesandstructures")],
    'subscript':        [_book("subscripts")],
    'super':            [_book("inheritance")],
    'switch':           [_book("controlflow")],
    '@State':           [_apple(APPLE_SWIFTUI, "state", "SwiftUI.State")],
    '@StateObject':     [_apple(APPLE_SWIFTUI, "stateobject", "SwiftUI.StateObject")],
    '@SceneStorage':    [_apple(APPLE_SWIFTUI, "scenestorage", "SwiftUI.SceneStorage")],
    '@Sendable':        [_evo("0302-concurrent-value-and-concurrent-closures.md", "Sendable (SE-0302)")],
    '#selector':        [_book("statements")],

    # T
    'Task':             [_apple(APPLE_SWIFT, "task", "Swift.Task (std lib)"), _book("concurrency")],
    'TaskGroup':        [_apple(APPLE_SWIFT, "taskgroup", "Swift.TaskGroup (std lib)")],
    'throw':            [_book("errorhandling")],
    'throws':           [_book("errorhandling"), _evo("0413-typed-throws.md", "Typed Throws (SE-0413)")],
    'true':             [_apple(APPLE_SWIFT, "bool", "Swift.Bool (std lib)")],
    'try':              [_book("errorhandling")],
    'typealias':        [_book("declarations")],
    '@testable':        [_book("attributes")],

    # U
    'unowned':          [_book("automaticreferencecounting")],
    '@UIApplicationMain':[_book("attributes")],

    # V
    'var':              [_book("thebasics")],
    'Void':             [_apple(APPLE_SWIFT, "void", "Swift.Void typealias")],

    # W
    'weak':             [_book("automaticreferencecounting")],
    'where':            [_book("generics")],
    'while':            [_book("controlflow")],
    '#warning':         [_book("statements")],

    # X
    'XMLParser':        [_apple(APPLE_FOUNDATION, "xmlparser", "Foundation.XMLParser")],

    # Z
    'ZStack':           [_apple(APPLE_SWIFTUI, "zstack", "SwiftUI.ZStack")],
}
