import SwiftUI

/// Displays the results of a generation job including detected
/// attributes, comparable listings, price band and templated copy.  It
/// also provides buttons to copy individual pieces of text or share
/// everything via the iOS share sheet.
struct GenerateView: View {
    let job: UserJob?
    @State private var showShareSheet = false
    @State private var shareItems: [Any] = []

    var body: some View {
        ScrollView {
            if let job = job {
                VStack(alignment: .leading, spacing: 16) {
                    // Detected attributes
                    Group {
                        Text("Detected Attributes")
                            .font(.headline)
                        if let category = job.detected.category {
                            Text("Category: \(category)")
                        }
                        if let brand = job.detected.brand {
                            Text("Brand: \(brand)")
                        }
                        if let model = job.detected.model {
                            Text("Model: \(model)")
                        }
                        if let color = job.detected.color {
                            Text("Color: \(color)")
                        }
                        if let size = job.detected.size {
                            Text("Size: \(size)")
                        }
                        if let condition = job.detected.condition {
                            Text("Condition: \(condition)")
                        }
                        if let features = job.detected.notable_features, !features.isEmpty {
                            Text("Features:")
                            ForEach(features, id: \.self) { feature in
                                Text("• \(feature)")
                            }
                        }
                    }

                    // Price band
                    Group {
                        Text("Suggested Price Range")
                            .font(.headline)
                        Text(String(format: "$%.2f – $%.2f (mid: $%.2f)", job.suggestedPrice.low, job.suggestedPrice.high, job.suggestedPrice.mid))
                        Text(String(format: "Confidence: %.0f%%", job.suggestedPrice.confidence * 100))
                    }

                    // Copy section
                    Group {
                        Text("Generated Copy")
                            .font(.headline)
                        Text(job.copy.title)
                            .fontWeight(.semibold)
                        ForEach(job.copy.bullets, id: \.self) { bullet in
                            Text("• \(bullet)")
                        }
                        HStack {
                            Button(action: { copyToClipboard(job.copy.title) }) {
                                Text("Copy Title")
                                    .padding(8)
                                    .background(Color.secondaryColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(6)
                            }
                            Button(action: { copyToClipboard(job.copy.bullets.joined(separator: "\n")) }) {
                                Text("Copy Description")
                                    .padding(8)
                                    .background(Color.secondaryColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(6)
                            }
                            Button(action: { copyToClipboard(fullText(for: job)) }) {
                                Text("Copy All")
                                    .padding(8)
                                    .background(Color.secondaryColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(6)
                            }
                            Button(action: {
                                shareItems = [fullText(for: job)]
                                showShareSheet = true
                            }) {
                                Text("Share")
                                    .padding(8)
                                    .background(Color.secondaryColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(6)
                            }
                        }
                    }

                    // Comps
                    Group {
                        Text("Comparables")
                            .font(.headline)
                        ForEach(job.comps.prefix(10)) { comp in
                            VStack(alignment: .leading) {
                                Text(comp.title)
                                    .fontWeight(.semibold)
                                Text(String(format: "$%.2f", comp.price))
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 4)
                        }
                    }
                }
                .padding()
            } else {
                Text("No job to display")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
        .navigationTitle("Results")
        .sheet(isPresented: $showShareSheet) {
            ActivityView(activityItems: shareItems)
        }
    }

    private func fullText(for job: UserJob) -> String {
        let bullets = job.copy.bullets.joined(separator: "\n")
        return "\(job.copy.title)\n\n\(bullets)"
    }

    private func copyToClipboard(_ text: String) {
        #if canImport(UIKit)
        UIPasteboard.general.string = text
        #endif
    }
}

struct GenerateView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            GenerateView(job: nil)
        }
    }
}