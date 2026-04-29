# Chapter 22: AI Chatbot Integration

**Claude's Swift Reference 26** -- Part VI: The Modern Toolchain

---

This chapter has two halves, one for each direction AI shows up in modern app development.

**Part A** is about **AI inside Xcode** -- the coding assistant that sits next to your editor and helps you write, refactor, document, and debug your code. You don't write any of this yourself; Apple ships it as part of Xcode 26. You configure it, you use it, you become more productive.

**Part B** is about **AI inside the apps you ship** -- calling a third-party AI service (like Anthropic's Claude or OpenAI's GPT) from Swift code so your own app can offer chat, summarization, completion, or any other AI feature to your users. This is networking + Codable + Keychain plumbing on top of an HTTP API.

Most readers will use Part A daily and Part B occasionally. Both are worth knowing. Read whichever side you need first.

---

# Part A: AI Inside Xcode (Coding Intelligence)

## The Three Layers

Xcode 26 ships three layers of AI that work together. Apple groups them under the umbrella term **"coding intelligence"** [^1].

### 1. Predictive Code Completion

An on-device machine-learning model, trained for Swift and the Apple SDKs, that predicts what you're about to type. Inline ghost-text suggestions appear as you write; Tab accepts. Runs entirely on Apple silicon, so no code leaves your Mac and the suggestions are responsive even offline. [^1]

This is the layer you'll touch every minute of every coding session. It's especially good at remembering parameter labels, recognizing API patterns from Apple's frameworks, and finishing trivial mechanical lines (the second branch of an `if let`, the matching close in a `do`/`catch`, the boilerplate `init` after a few `var` declarations).

### 2. Coding Tools

In-source-editor menu commands for AI-assisted writing tasks. Apple frames it as *"like Writing Tools, but for code"*: select a chunk of code or a doc comment, right-click, choose a Coding Tool from the menu, and the tool either rewrites in place or proposes a diff you accept or reject. [^1]

The built-in tools cover the common cases: write a doc comment for this function, fix this error, explain what this code does, refactor for clarity, generate a unit test stub. You don't have to type a prompt; the tool's built-in instruction is appropriate to the editor selection.

### 3. LLM Integration with External Agents

Xcode 26 supports interacting with your code through a chat panel powered by a large language model of your choice -- Anthropic's **Claude Agent** and OpenAI's **Codex** are the documented options today, with one-click download and auto-update. [^1]

The interaction is built on the **Model Context Protocol** (MCP), an open standard, so any MCP-compliant agent or tool can plug into Xcode the same way. [^2]

## Agentic Coding (Xcode 26.3)

The most capable mode is **agentic coding**, introduced in Xcode 26.3. The agent doesn't just answer one question and stop -- it operates autonomously over multi-step tasks. [^2]

Apple's published Tech Talk demonstrates the agent adding WeatherKit-driven 7-day-forecast functionality to a Landmarks sample app. The agent autonomously:

- Familiarizes itself with the project's file structure and existing code
- Searches Apple's documentation for the modern Liquid Glass API
- Generates 400+ lines of code across three new files
- Adds the WeatherKit entitlement to the project configuration
- Builds, detects errors, fixes them, and iterates until the build succeeds [^2]

What used to be a back-and-forth conversation -- you ask, the AI answers, you copy-paste, you run, you report errors back, the AI proposes fixes, you copy-paste again -- becomes a single instruction the agent carries out end to end. You're free to think about the next feature while the current one builds.

## Configuring Your LLM Choice

Apple's documentation for setting this up is at `developer.apple.com/documentation/Xcode/setting-up-coding-intelligence`. [^3] The short version:

1. Open Xcode's settings (**Xcode > Settings**, or `⌘,`).
2. Find the **Intelligence** pane (the exact label may shift between minor versions).
3. Click the LLM provider you want -- Claude Agent or Codex.
4. Sign in to your provider account; Xcode handles the OAuth flow and the agent download.
5. Use the chat sidebar to start asking questions about your project.

The agent runs locally; the LLM call goes out to Anthropic or OpenAI. If you'd rather stay fully on-device, Predictive Code Completion alone handles a lot without any network call. The agent layer is for when you want a partner that can read your codebase and hold a longer conversation.

## When to Use Which Layer

- **Predictive Code Completion** -- always on, every line, no thought required. Tab to accept, ignore otherwise.
- **Coding Tools** -- when you want to do one specific transform on a chunk of code (write doc comments, fix this error, explain this). Right-click and pick.
- **External agent (Claude / Codex)** -- when you want a real conversation about a multi-step task, or when you want the agent to act autonomously across multiple files (Xcode 26.3+).

A good habit: turn on Predictive Code Completion the moment you install Xcode (it's defaults-on but worth verifying). Reach for Coding Tools when an inline transform fits. Reach for the external agent when you'd otherwise send a friend an email starting *"so I'm trying to add..."* -- that's when an agent earns its keep.

## What's Coming

This chapter's Part A is what's documented and shipping at the time this Bible was written. WWDC 26 in June 2026 is expected to expand the integrated-AI story significantly; this chapter gets a major refresh after that announcement.

[^1]: [Xcode -- Apple Developer](https://developer.apple.com/xcode/?cid=ht-xcode)
[^2]: [Meet agentic coding in Xcode (Apple Developer Tech Talk)](https://developer.apple.com/videos/play/tech-talks/111428/)
[^3]: [Setting up coding intelligence (Apple Developer Documentation)](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence)

---

# Part B: AI Inside Your Own App (Third-Party API Integration)

The rest of this chapter teaches you to call a third-party AI service from Swift code -- the path you take when you want your own app to offer chat, summarization, or completion to your users. The example uses Anthropic's Claude API, but the pattern (HTTP request, JSON in, JSON out, Keychain for the key) is identical for any text-completion API on the market.

## What You'll Learn (Part B)

By the end of Part B you can:

- Register an Anthropic Claude API account, get an API key, and make your first call from Swift.
- Send a message to Claude from an iOS or Mac app using only `URLSession` and `Codable`.
- Store the API key safely in the Keychain instead of hard-coding it.
- Build a minimal chat view that streams the assistant's reply as it arrives.

---

## What the Anthropic API Is

Anthropic's Claude API is an HTTP JSON service. You POST a request describing the conversation so far; you receive a JSON response containing Claude's next message. No special SDK is required -- `URLSession` and `Codable` are enough.

### Getting an API Key

1. Sign up at `console.anthropic.com`.
2. Fund the account or use the free tier's trial credits.
3. Create an API key from the Keys section. Copy it once; Anthropic will not show it again.

Treat the key like a password. Never commit it to Git, never paste it in chat, never embed it in client-side code that ships to end users (see the "Production" note at the end of the chapter).

---

## The Request Shape

A minimal chat request looks like this:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    { "role": "user", "content": "Hello, Claude." }
  ]
}
```

Send it as the body of a `POST https://api.anthropic.com/v1/messages`, with these headers:

```
x-api-key: <your key>
anthropic-version: 2023-06-01
content-type: application/json
```

The response is JSON containing Claude's reply.

---

## A Minimal Swift Client

### The Codable Types

```swift
struct ChatRequest: Codable {
    let model: String
    let max_tokens: Int
    let messages: [Message]
}

struct Message: Codable {
    let role: String       // "user" or "assistant"
    let content: String
}

struct ChatResponse: Codable {
    let content: [ContentBlock]
    struct ContentBlock: Codable {
        let type: String   // "text"
        let text: String
    }
}
```

### The Call

```swift
import Foundation

enum ChatError: Error {
    case badStatus(Int, String)
    case noText
}

func send(_ history: [Message], apiKey: String) async throws -> String {
    var request = URLRequest(url: URL(string: "https://api.anthropic.com/v1/messages")!)
    request.httpMethod = "POST"
    request.setValue(apiKey,             forHTTPHeaderField: "x-api-key")
    request.setValue("2023-06-01",       forHTTPHeaderField: "anthropic-version")
    request.setValue("application/json", forHTTPHeaderField: "content-type")

    let payload = ChatRequest(
        model:      "claude-sonnet-4-6",
        max_tokens: 1024,
        messages:   history
    )
    request.httpBody = try JSONEncoder().encode(payload)

    let (data, response) = try await URLSession.shared.data(for: request)
    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
        let body = String(data: data, encoding: .utf8) ?? ""
        let code = (response as? HTTPURLResponse)?.statusCode ?? -1
        throw ChatError.badStatus(code, body)
    }

    let decoded = try JSONDecoder().decode(ChatResponse.self, from: data)
    guard let text = decoded.content.first(where: { $0.type == "text" })?.text else {
        throw ChatError.noText
    }
    return text
}
```

Usage:

```swift
Task {
    let reply = try await send(
        [Message(role: "user", content: "Summarize the Gettysburg Address in one sentence.")],
        apiKey: "sk-ant-..."
    )
    print(reply)
}
```

That's the whole non-streaming path. Every chat feature is a variation on this.

---

## Storing the API Key Safely

### Do Not Hard-Code It

```swift
let apiKey = "sk-ant-ExamplePlease"   // 🚫 ships in your binary
```

Anyone who unzips your app bundle can read the binary's strings and pull the key. Treat hard-coding as identical to posting the key publicly.

### The Keychain -- For User-Provided Keys

The safest pattern for a user-brings-their-own-key app: have the user paste their key into a settings view; store it in the Keychain; read it at call time.

Minimal Keychain wrapper:

```swift
import Security

enum Keychain {
    private static let service = "com.yourname.YourApp"

    static func save(_ value: String, for key: String) throws {
        let data = Data(value.utf8)
        let query: [String: Any] = [
            kSecClass as String:       kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
        ]
        SecItemDelete(query as CFDictionary)

        var attrs = query
        attrs[kSecValueData as String] = data
        let status = SecItemAdd(attrs as CFDictionary, nil)
        if status != errSecSuccess { throw NSError(domain: "Keychain", code: Int(status)) }
    }

    static func load(_ key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String:       kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String:  true,
            kSecMatchLimit as String:  kSecMatchLimitOne,
        ]
        var ref: CFTypeRef?
        guard SecItemCopyMatching(query as CFDictionary, &ref) == errSecSuccess,
              let data = ref as? Data,
              let str = String(data: data, encoding: .utf8) else {
            return nil
        }
        return str
    }
}
```

Save once when the user enters the key:

```swift
try Keychain.save(userEnteredKey, for: "anthropicAPIKey")
```

Load at call time:

```swift
guard let key = Keychain.load("anthropicAPIKey") else {
    // prompt the user to enter it
    return
}
let reply = try await send(messages, apiKey: key)
```

---

## A Minimal Chat View

```swift
import SwiftUI

struct ChatView: View {
    @State private var history: [Message] = []
    @State private var draft: String = ""
    @State private var sending = false
    @State private var errorText: String?

    var body: some View {
        VStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 12) {
                    ForEach(history.indices, id: \.self) { i in
                        Bubble(message: history[i])
                    }
                }
                .padding()
            }

            if let errorText {
                Text(errorText).foregroundStyle(.red).padding(.horizontal)
            }

            HStack {
                TextField("Ask Claude...", text: $draft)
                    .textFieldStyle(.roundedBorder)
                Button("Send") { Task { await send() } }
                    .disabled(draft.isEmpty || sending)
            }
            .padding()
        }
    }

    private func send() async {
        let userMsg = Message(role: "user", content: draft)
        history.append(userMsg)
        draft = ""
        sending = true
        errorText = nil

        do {
            guard let key = Keychain.load("anthropicAPIKey") else {
                errorText = "No API key set. Add one in Settings."
                sending = false
                return
            }
            let reply = try await SwiftReference26.send(history, apiKey: key)
            history.append(Message(role: "assistant", content: reply))
        } catch {
            errorText = error.localizedDescription
        }
        sending = false
    }
}

struct Bubble: View {
    let message: Message
    var body: some View {
        HStack {
            if message.role == "assistant" { Spacer(minLength: 40) }
            Text(message.content)
                .padding(10)
                .background(message.role == "user" ? Color.blue : Color.gray.opacity(0.2),
                            in: RoundedRectangle(cornerRadius: 12))
                .foregroundStyle(message.role == "user" ? .white : .primary)
            if message.role == "user" { Spacer(minLength: 40) }
        }
    }
}

enum SwiftReference26 {
    static func send(_ history: [Message], apiKey: String) async throws -> String {
        // The `send` function defined earlier in the chapter.
        try await Claudes_X26_Swift6_Bible.send(history, apiKey: apiKey)
    }
}
```

Run it. Type a message, tap Send, wait a second or two, Claude's reply appears in a gray bubble. Every message so far is appended to `history` and re-sent on the next call, giving the model the running context.

---

## Streaming Responses

When the reply is long, waiting for the full JSON to arrive feels slow. Anthropic supports Server-Sent Events streaming. You pass `"stream": true` in the request, and the response is a sequence of events you read as they arrive.

```swift
var request = URLRequest(url: URL(string: "https://api.anthropic.com/v1/messages")!)
request.httpMethod = "POST"
request.setValue(apiKey, forHTTPHeaderField: "x-api-key")
request.setValue("2023-06-01", forHTTPHeaderField: "anthropic-version")
request.setValue("application/json", forHTTPHeaderField: "content-type")

let body = """
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "stream": true,
  "messages": [{ "role": "user", "content": "Hello!" }]
}
"""
request.httpBody = body.data(using: .utf8)

let (bytes, _) = try await URLSession.shared.bytes(for: request)
for try await line in bytes.lines {
    // Each SSE event is "event: xyz\n" then "data: {...json...}\n\n".
    if line.hasPrefix("data: ") {
        let json = String(line.dropFirst("data: ".count))
        // Parse and append any "text_delta" content to the assistant's message on screen.
    }
}
```

The UI binding pattern: hold the assistant's growing text in a `@State` string, append each delta as it arrives, and SwiftUI repaints the bubble on every update. The user sees Claude "typing" in real time.

---

## Production Notes

- **Don't ship your own API key in a client app.** For apps where you (not the user) are paying for inference, proxy through a server you control. The server holds the key; the app calls your server. This gives you rate limiting, per-user auth, and a way to rotate the key without re-releasing the app.
- **User-brings-their-own-key apps** (the pattern in this chapter) are fine for hobby and internal-tool apps. Store the key in Keychain as shown.
- **Check the model catalog before shipping.** Anthropic retires older models on a schedule; link to `docs.anthropic.com` in your app's help so users know which model is current.
- **Budget for it.** The API bills per input + output token. A long conversation with a large `max_tokens` setting can run up a meaningful bill without warning. Show the user the current month-to-date cost if your app supports it.

---

## Chapter Mini-Example -- Settings Screen for the API Key

A place for users to paste their key and stash it in the Keychain:

```swift
import SwiftUI

struct SettingsView: View {
    @State private var keyField = ""
    @State private var savedNote: String?

    var body: some View {
        Form {
            Section("Anthropic API Key") {
                SecureField("sk-ant-...", text: $keyField)
                Button("Save") {
                    do {
                        try Keychain.save(keyField, for: "anthropicAPIKey")
                        keyField = ""
                        savedNote = "Key saved."
                    } catch {
                        savedNote = "Could not save: \(error.localizedDescription)"
                    }
                }
                if let savedNote {
                    Text(savedNote).foregroundStyle(.secondary)
                }
            }
            Section {
                Link("Get a key from Anthropic",
                     destination: URL(string: "https://console.anthropic.com")!)
            }
        }
        .navigationTitle("Settings")
    }
}
```

The user pastes, the app keychains, the `ChatView` reads it back, and you have a real, working chat app talking to a real model.

---

## End of Part VI

That's the modern toolchain: version control, a remote, and a live AI backend you can reach in a few lines of Swift. Appendices A through D walk you through four complete companion apps that exercise what you've learned across all six Parts.
