# Chapter 17: Swift Charts & PDFKit

**Claude's Swift Reference 26** -- Part IV: The Application

---

## What You'll Learn

By the end of this chapter you can:

- Draw bar, line, point, and area charts with Swift Charts using your own data.
- Customize the axes, labels, and colors without leaving SwiftUI.
- Render a SwiftUI view into a PDF you can share or print.
- Load, display, and page through an existing PDF document with PDFKit.

---

## Swift Charts

Swift Charts arrived with iOS 16 / macOS 13 and now lives across every Apple platform. It's SwiftUI for data visualization: you describe what you want to draw, the framework handles layout, ticks, legends, and animation.

### The Basic Shape

Every chart starts with `Chart` and one or more mark types inside.

```swift
import Charts
import SwiftUI

struct Sale: Identifiable {
    let id = UUID()
    let day: String
    let amount: Double
}

struct WeekSales: View {
    let sales: [Sale] = [
        .init(day: "Mon", amount: 120),
        .init(day: "Tue", amount: 80),
        .init(day: "Wed", amount: 140),
        .init(day: "Thu", amount: 90),
        .init(day: "Fri", amount: 200),
        .init(day: "Sat", amount: 160),
        .init(day: "Sun", amount: 110),
    ]

    var body: some View {
        Chart(sales) { sale in
            BarMark(
                x: .value("Day", sale.day),
                y: .value("Sales", sale.amount)
            )
        }
        .frame(height: 240)
        .padding()
    }
}
```

The `.value(_:_:)` pairs name the axis and the value; the name appears in labels, VoiceOver callouts, and accessibility summaries.

### Mark Types

Swap `BarMark` for any of these depending on the story your data tells:

- `BarMark` -- counts, totals, comparisons between categories.
- `LineMark` -- trends over a continuous variable, usually time.
- `PointMark` -- scatter plots.
- `AreaMark` -- cumulative totals, filled region under a line.
- `RuleMark` -- a horizontal or vertical guide line (averages, thresholds).
- `RectangleMark` -- heat-map cells or day-range highlights.

You can combine them. A line with points and an average line:

```swift
Chart(sales) { sale in
    LineMark(x: .value("Day", sale.day),
             y: .value("Sales", sale.amount))
    PointMark(x: .value("Day", sale.day),
              y: .value("Sales", sale.amount))
}
.chartYAxis {
    AxisMarks(position: .leading)
}
```

### Series (Color-Coded Groups)

If your data has a category dimension, `.foregroundStyle(by:)` splits it into color-coded series:

```swift
struct Revenue: Identifiable {
    let id = UUID()
    let month: String
    let store: String
    let amount: Double
}

Chart(data) { r in
    BarMark(x: .value("Month", r.month),
            y: .value("Revenue", r.amount))
        .foregroundStyle(by: .value("Store", r.store))
}
```

Swift Charts picks colors, adds a legend, and handles stacking. For side-by-side bars instead of stacked, add `.position(by: .value("Store", r.store))`.

### Axes and Labels

Most of the time the defaults are good. When you want control:

```swift
Chart(sales) { sale in
    BarMark(x: .value("Day", sale.day),
            y: .value("Sales", sale.amount))
}
.chartXAxis {
    AxisMarks { value in
        AxisValueLabel()
            .font(.caption)
        AxisGridLine()
    }
}
.chartYAxis {
    AxisMarks(position: .leading, values: .stride(by: 50)) { value in
        AxisGridLine()
        AxisValueLabel { Text("$\(value.as(Int.self) ?? 0)") }
    }
}
```

### Interactivity

Swift Charts supports selection out of the box on iOS 17 / macOS 14 and later:

```swift
@State private var selectedDay: String?

Chart(sales) { sale in
    BarMark(x: .value("Day", sale.day),
            y: .value("Sales", sale.amount))
}
.chartXSelection(value: $selectedDay)
```

Tap a bar and `selectedDay` updates. Combine with an overlay to show a callout.

---

## PDFKit

PDFKit is Apple's framework for reading, displaying, and composing PDF documents. Two tasks cover 95% of what apps need: **render a SwiftUI view to PDF** and **display an existing PDF**.

### Rendering a View to PDF

`ImageRenderer` (iOS 16+) renders any SwiftUI view into a bitmap or PDF-backed CGContext. This is how you make a printable receipt, report, or share-as-PDF feature.

```swift
import SwiftUI

@MainActor
func renderPDF<Content: View>(
    _ view: Content,
    to url: URL,
    size: CGSize = .init(width: 8.5 * 72, height: 11 * 72)
) throws {
    let renderer = ImageRenderer(content:
        view.frame(width: size.width, height: size.height)
    )

    try renderer.render { _, context in
        var box = CGRect(origin: .zero, size: size)
        guard let pdf = CGContext(url as CFURL, mediaBox: &box, nil) else {
            return
        }
        pdf.beginPDFPage(nil)
        context(pdf)
        pdf.endPDFPage()
        pdf.closePDF()
    }
}
```

Usage:

```swift
let url = URL.temporaryDirectory.appending(path: "receipt.pdf")
try renderPDF(ReceiptView(order: order), to: url)
// Hand url to ShareLink, UIActivityViewController, or UIDocumentInteractionController.
```

Book 14's `ShareLink` accepts a file URL, so you can ship the PDF with one call.

### Displaying a PDF

`PDFView` from PDFKit wraps into SwiftUI via `UIViewRepresentable` (or `NSViewRepresentable` on Mac):

```swift
import SwiftUI
import PDFKit

struct PDFReader: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> PDFView {
        let v = PDFView()
        v.document = PDFDocument(url: url)
        v.autoScales = true
        v.displayMode = .singlePageContinuous
        return v
    }

    func updateUIView(_ v: PDFView, context: Context) {
        if v.document?.documentURL != url {
            v.document = PDFDocument(url: url)
        }
    }
}
```

Drop it into a view:

```swift
struct PDFScreen: View {
    let url: URL

    var body: some View {
        PDFReader(url: url)
            .ignoresSafeArea()
    }
}
```

`PDFView` gives you pinch-to-zoom, page navigation, and built-in selection highlighting for free.

### Paging, Search, and Outline

- **Page count**: `document.pageCount`.
- **Specific page**: `document.page(at: 0)` returns a `PDFPage`.
- **Search**: `document.findString("swift", withOptions: .caseInsensitive)` returns an array of `PDFSelection`.
- **Outline**: `document.outlineRoot` returns the PDF's table of contents if it has one.

---

## Chapter Mini-Example -- Bar Chart with Export

```swift
import SwiftUI
import Charts

struct Sale: Identifiable {
    let id = UUID()
    let day: String
    let amount: Double
}

struct SalesDashboard: View {
    let sales: [Sale] = [
        .init(day: "Mon", amount: 120),
        .init(day: "Tue", amount: 80),
        .init(day: "Wed", amount: 140),
        .init(day: "Thu", amount: 90),
        .init(day: "Fri", amount: 200),
        .init(day: "Sat", amount: 160),
        .init(day: "Sun", amount: 110),
    ]

    @State private var pdfURL: URL?

    var body: some View {
        VStack {
            chart
            if let url = pdfURL {
                ShareLink(item: url) { Label("Share PDF", systemImage: "square.and.arrow.up") }
            } else {
                Button("Export to PDF") { exportPDF() }
            }
        }
        .padding()
    }

    private var chart: some View {
        Chart(sales) { sale in
            BarMark(x: .value("Day", sale.day),
                    y: .value("Sales", sale.amount))
        }
        .frame(height: 260)
    }

    @MainActor
    private func exportPDF() {
        let url = URL.temporaryDirectory.appending(path: "weekly-sales.pdf")
        let renderer = ImageRenderer(content:
            chart.frame(width: 600, height: 400).padding()
        )
        renderer.render { _, context in
            var box = CGRect(x: 0, y: 0, width: 612, height: 792)
            guard let pdf = CGContext(url as CFURL, mediaBox: &box, nil) else { return }
            pdf.beginPDFPage(nil)
            context(pdf)
            pdf.endPDFPage()
            pdf.closePDF()
        }
        pdfURL = url
    }
}
```

One view, a chart, and a button that exports the chart to a real PDF the user can share. That's the pattern for reports throughout the rest of your career.

---

## What Book 18 Does

Book 17 drew what we had. Book 18 covers what to do when things break: Swift's error-handling system -- `throws`, `try`, `catch`, typed throws in Swift 6, and the `Result` type for callback-era APIs.
