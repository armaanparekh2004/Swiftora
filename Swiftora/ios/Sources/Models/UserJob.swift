import Foundation

/// Represents the detected attributes of an uploaded item.
struct Detected: Codable, Identifiable {
    var id: UUID { UUID() }
    let category: String?
    let brand: String?
    let model: String?
    let color: String?
    let size: String?
    let condition: String?
    let notable_features: [String]?
    let defects: [String]?
}

/// Represents a comparable listing used to inform pricing.
struct Comp: Codable, Identifiable {
    var id: UUID { UUID() }
    let source: String
    let url: String
    let price: Double
    let currency: String
    let title: String
    let image: String?
    let condition: String?
    let shipping: Double?
}

/// Represents the suggested price band derived from comps.
struct SuggestedPrice: Codable {
    let low: Double
    let mid: Double
    let high: Double
    let confidence: Double
}

/// Represents the templated copy used for the listing title and bullet points.
struct GeneratedCopy: Codable {
    let title: String
    let bullets: [String]
}

/// The top level job structure returned from the backend and persisted locally.
struct UserJob: Codable, Identifiable {
    let id: String
    let userId: String
    let imageUrl: String
    let notes: String?
    let detected: Detected
    let comps: [Comp]
    let suggestedPrice: SuggestedPrice
    let copy: GeneratedCopy
    let createdAt: String
}