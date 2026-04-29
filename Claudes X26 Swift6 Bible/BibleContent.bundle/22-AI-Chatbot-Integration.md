# Chapter 22: AI Chatbot Integration

**Claude's Swift Reference 26** -- Part VI: The Modern Toolchain

---

## What You'll Learn

By the end of this chapter you can:

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
