import Foundation
import Alamofire
import UIKit

/// Service responsible for communicating with the local Swiftora backend.
final class APIService {
    /// Shared singleton instance for convenience.
    static let shared = APIService()
    private init() {}

    /// Base URL for the backend.  In Demo Mode this should point to
    /// localhost.  In Live Mode it could be updated via configuration.
    private let baseURL = URL(string: "http://localhost:8000")!

    /// Perform analysis on an image and optional notes.  On success the
    /// backend returns a fully populated `UserJob` which is delivered
    /// through the completion handler on the main thread.
    func analyze(image: UIImage, notes: String?, userId: String, completion: @escaping (Result<UserJob, Error>) -> Void) {
        let url = baseURL.appendingPathComponent("/analyze")

        // Prepare JPEG data
        guard let jpegData = image.jpegData(compressionQuality: 0.7) else {
            completion(.failure(APIError.invalidImage))
            return
        }

        // Build multipart form data
        AF.upload(multipartFormData: { multipart in
            multipart.append(jpegData, withName: "file", fileName: "upload.jpg", mimeType: "image/jpeg")
            if let notes = notes {
                multipart.append(Data(notes.utf8), withName: "notes")
            }
            multipart.append(Data(userId.utf8), withName: "userId")
        }, to: url)
        .responseDecodable(of: UserJob.self) { response in
            DispatchQueue.main.async {
                switch response.result {
                case .success(let job):
                    completion(.success(job))
                case .failure(let error):
                    completion(.failure(error))
                }
            }
        }
    }

    enum APIError: Error {
        case invalidImage
    }
}