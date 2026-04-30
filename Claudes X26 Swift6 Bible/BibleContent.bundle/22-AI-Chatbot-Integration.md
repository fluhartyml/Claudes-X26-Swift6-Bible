# Chapter 22: AI Chatbot Integration

**Claude's Swift Reference 26** -- Part VI: The Modern Toolchain

---

## Chapter Overview — Three Paths to AI in X26

X26 ships AI in three distinct places, and the chapter is organized around them. Each path serves a different need; most readers will reach for one but should know all three exist:

- **Part A — AI inside Xcode (Coding Intelligence).** The chat panel and agentic-coding features built into Xcode 26. You're the developer using AI to write code faster. Apple article: *Writing code with intelligence in Xcode*.
- **Part B — AI inside your own app (Foundation Models).** Apple's first-party on-device LLM framework. No API key, no network round-trip, no per-token cost. Apple article: *Generating content and performing tasks with Foundation Models*.
- **Part C — Third-party API integration (Anthropic, etc.).** When you need capabilities the on-device model doesn't cover — bigger context windows, more demanding reasoning, model choices Apple doesn't ship — you call out to a vendor's REST API. The original chapter content for X26's first edition.

Volume 1 of this book ships Parts A and C. Part B is being drafted next.

---

## Part A — AI Inside Xcode (Coding Intelligence)

The coding intelligence features in Xcode help you write code, navigate unfamiliar codebases, find opportunities for new features, fix or refactor existing code, and generate documentation along the way[^a1]. You interact with a large language model using natural language prompts to ask questions and give instructions; the model refines its responses based on your previous interactions and project context.

### Two Shapes of Help — Agent vs Chat

Apple distinguishes two ways of working with the coding assistant, and the distinction is load-bearing for everything that follows. There's also a quieter cost-and-cap distinction sitting underneath the choice that matters in practice.

**An agent** — in Apple's words — *"can refine and iterate on a goal with less guidance and perform actions, such as fixing build errors after writing code. You decide what external tools, command-line or otherwise, an agent may use in responses to your prompts."*[^a1] When an agent needs to read a file or run a tool, Xcode pops up a permission dialog. The two agents Apple ships with are Anthropic's Claude Agent and OpenAI's Codex, both wired in via the **Model Context Protocol (MCP)**, an open standard.

**A chat product** — *"you stay in control over changes to your project by applying suggestions automatically or reviewing and applying them selectively yourself."*[^a1] Chat products do not act on your project on their own. Two chat-only toggles live in the lower-right corner of the assistant sidebar: *Automatically apply code changes* (on by default) and *Project Context* (on by default). Agents do not show those toggles because they have their own permissioned access to the project.

### The Cost and Usage-Cap Distinction Apple Doesn't Spell Out

The agent and chat paths use different authentication and billing models, and Apple's article skips this part:

- **Claude (chat) in the Intelligence panel** connects to Anthropic's REST API directly via an API key. You set the key up at `console.anthropic.com`, fund the account, and Xcode bills **per token** against that funded balance. Every prompt and every response is metered against money you put in up front.
- **Claude Agent** (the agentic-coding path added in Xcode 26.3) signs in with your existing Claude subscription via OAuth. No per-token meter — the agent's usage is included in the subscription tier. The recurring "Claude OAuth token expired" fix in Xcode's release notes is for this path's auth flow, not the API-key path.
- **OpenAI's Codex** agent and ChatGPT chat split the same way — agent by subscription OAuth, chat by API key.

The third axis Apple also doesn't mention is **usage caps**. Consumer chat subscriptions (Claude.ai, ChatGPT.com) have time-window caps that reset on a cycle — if you're in a heavy back-and-forth, you can hit the cap mid-task and have to wait for the window to reset. The agent / CLI path uses a different cap model that, in practice, lets long autonomous sessions run without you noticing the limit. The API-key chat path has no time-window cap at all — only rate limits and the funded balance — so heavy sessions cost more rather than pause.

The practical read: the subscription-based agent path is the closest experience to "flat-rate, runs as long as you need it." The consumer-chat-product feel of flat-rate works until the time window resets you out. The API-key chat path is metered — longer conversations and bigger context windows cost more, but they don't pause.

### Opening the Coding Assistant

Press **Command-0** or click the button to the right of the Navigator button in the upper-left of the toolbar. The assistant opens in a sidebar.

If a *Set Up* button shows where the prompt field would normally be, no provider is enabled yet. Click it to land in **Xcode > Settings > Intelligence** and enable a provider per Apple's *Setting up coding intelligence* article[^a2].

To start a fresh conversation, click the *Start New Conversation* button on the left of the assistant's toolbar. The pop-up menu separates **Agents** (one heading) from **Chat** models (a second heading). The provider you pick shows up in the message field and is the one that handles the next prompt.

### Asking the Assistant to Explain Code

The lowest-stakes way to start is asking the model to explain code that already exists. Open any project — Apple uses the Landmarks sample app in their walkthrough — and type a free-form question into the assistant:

```
What does this app do?
```

The model's reply appears under the prompt. Replies are interactive. If a reply mentions a filename, an arrow button next to the filename opens it in the source editor. Follow-up prompts continue the same conversation.

### Asking About a Specific Symbol

For a question scoped to a piece of code in front of you, Control-click the symbol or selection in the source editor and choose **Show Coding Tools > Show Coding Tools** from the contextual menu. **Command-Option-0** does the same thing without the menu trip. Either way the *coding tools popover* appears.

Click **Explain** for Apple's default question, or type a more specific prompt into the popover. The same coding tools popover is also reachable from the coding intelligence icon in the source editor's gutter.

### Generating or Modifying Code

Type a free-form prompt into the assistant. Apple's example sequence on a SwiftUI app, prompts in order:

- Add properties and methods to a class.
- Create a list view and wrap it in a NavigationStack.
- Add the ability to edit the properties of items in the list view.
- Change the list view to a table view showing all the properties.

Each prompt narrows the work and produces a small enough change to validate before moving on. Generated changes are highlighted with **multicolor change bars** in the gutter so they stand out from manual edits. The **Undo Changes** button to the right of the prompt field undoes the most recent batch.

If you picked an agent rather than a chat product, the agent may build the app to verify its changes and try to fix build warnings or errors automatically. That self-correction loop is the agent layer at work; chat products do not do it.

### Applying Changes (Chat-Product Path)

This section only applies to chat products. Agents bypass it by acting on the project directly under the permissions you grant.

The *Automatically apply code changes* toggle in the lower-right of the sidebar is on by default. Turning it off changes the assistant's behavior: instead of writing changes into your files, it labels each suggested change as **Proposal**. To apply a proposal, click the code snippet in the response and click **Apply** in the dialog. If the proposal adds a new file, the dialog reads **Create New File**.

### Adding Context to a Prompt

Xcode automatically gathers context for the prompt based on the open files, conversation history, and what you typed. You can also add context explicitly.

Type the `@` character in the prompt field and a completion menu appears with symbols and filenames. Pick one and the prompt now references that exact symbol or file. For files outside the project, choose *Upload files* from the Attachments pop-up menu in the lower-left.

Chat products have an additional toggle: **Project Context** (lower-right corner of the sidebar, on by default). With it on, the assistant can share relevant code from across the project with the model. Turn it off to scope the assistant to only the files and symbols you reference explicitly with `@`.

### Generating Playgrounds and Previews

The coding tools popover (Command-Option-0) has a **Generate a Playground** button. Click it on any function and Xcode inserts a `#Playground` macro with sample inputs. Results render in the canvas area; if the canvas is hidden, choose **Editor > Canvas** to show it and click **Resume**.

The `#Playground` macro is its own X26 feature, covered in detail in Apple's *Running code snippets using the playground macro* article[^a3].

### Fixing Errors with Generate Fix for Issue

The source editor underlines errors in red and shows an icon. Click the icon to expand the issue and you'll see *Generate Fix for Issue* with a **Generate** button. Clicking Generate sends the error to the model, applies the model's fix, and shows the change in the conversation area with the same multicolor change bars.

If you're working with an agent, the agent does this automatically for errors and warnings in code it has just generated.

### Generating Documentation

Select a symbol that needs documentation. Click the coding intelligence icon in the source editor gutter and choose **Document** in the coding tools popover. Xcode inserts **DocC-style comments** above the symbol. For a class, that means documentation for the class itself plus its properties and methods, including method parameters.

To browse the generated documentation in Xcode, choose **Product > Build Documentation**.

### Browsing Past Conversations

The conversation pop-up menu in the middle of the assistant's toolbar lists recent and previous conversations. Pick one and the assistant scrolls back through the prompts and responses for that thread. **Clear Recents** in the same menu removes them. Conversations are scoped per-project.

### Rolling a Project Back with Conversation History

This is the assistant's most powerful undo. From the conversation pop-up, pick the conversation, then click the **History** button. Xcode shows a chronological list of your prompts down the left and a slider down the right.

Slide up to remove changes from the top of the conversation backwards in time; slide down to restore them. As you move the slider, the source editor shows the project at that point in the conversation. **Restore** locks in the rolled-back state and Xcode keeps the later edits in case you decide to roll forward later. **Cancel** keeps everything as it was.

> **Required:** the project must be in a Git repository for History to work. If it isn't, Xcode prompts to create one with a *Create Repository* button. Equivalent menu path: **Integrate > New Git Repository**. Xcode does not modify the repository — History uses it for reference only.

### What This Replaces in Your Day

Most of the work this part covers used to live somewhere else: a separate browser tab with documentation open, a chat window with a third-party assistant, a fresh playground project for one-off experiments, a manual hunt for the right Fix-it, a hand-written DocC comment block. The coding assistant collapses those into the editor itself.

That collapse is the point. The keystrokes are short (Command-0, Command-Option-0), the context is automatic, and the assistant is one keystroke away whether you want explanation, generation, fix, or rollback.

[^a1]: Apple Developer Documentation, *Writing code with intelligence in Xcode*. <https://developer.apple.com/documentation/xcode/writing-code-with-intelligence-in-xcode> — verified 2026-04-29.
[^a2]: Apple Developer Documentation, *Setting up coding intelligence*. <https://developer.apple.com/documentation/xcode/setting-up-coding-intelligence>
[^a3]: Apple Developer Documentation, *Running code snippets using the playground macro*. <https://developer.apple.com/documentation/xcode/running-code-snippets-using-the-playground-macro>

---

## Part B — Foundation Models in Your Own App

*Drafting in progress. Part B covers Apple's on-device Foundation Models framework — the first-party answer to "I want my app to do AI itself." Sourced from Apple's "Generating content and performing tasks with Foundation Models" article, verified 2026-04-29. The full content lands in a follow-up commit.*

---

## Part C — Third-Party API Integration (Anthropic Claude)

When the on-device Foundation Models framework can't handle what your app needs — typically because the model is not suited for the use case (basic math, code generation, complex logical reasoning per Apple's own guidance), or because you need a context window larger than 4,096 tokens, or because you want a specific vendor's model — you call out to a third-party API. This part walks the reference implementation against Anthropic's Claude API.

This Part C content was the entire chapter in the book's first draft. It still teaches a useful integration pattern; it just sits in a different place in the chapter's structure now. Use it when on-device intelligence isn't a fit for the app you're building.

### What You'll Learn

By the end of Part C you can:

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
