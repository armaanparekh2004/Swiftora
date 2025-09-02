import XCTest
@testable import AppModule

final class SwiftoraTests: XCTestCase {
    func testUserJobDecoding() throws {
        let json = """
        {
          "id": "123",
          "userId": "user@example.com",
          "imageUrl": "path/to/image.jpg",
          "notes": "Some notes",
          "detected": {
            "category": "smartphone",
            "brand": "Apple",
            "model": "iPhone 12",
            "color": "blue",
            "size": "medium",
            "condition": "good",
            "notable_features": ["Feature A", "Feature B"],
            "defects": []
          },
          "comps": [],
          "suggestedPrice": {
            "low": 100.0,
            "mid": 150.0,
            "high": 200.0,
            "confidence": 0.8
          },
          "copy": {
            "title": "Apple iPhone 12",
            "bullets": ["Bullet 1", "Bullet 2"]
          },
          "createdAt": "2025-09-02T00:00:00Z"
        }
        """
        let data = Data(json.utf8)
        let decoder = JSONDecoder()
        let job = try decoder.decode(UserJob.self, from: data)
        XCTAssertEqual(job.userId, "user@example.com")
        XCTAssertEqual(job.detected.brand, "Apple")
        XCTAssertEqual(job.suggestedPrice.mid, 150.0)
        XCTAssertEqual(job.copy.bullets.count, 2)
    }
}