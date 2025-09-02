import Foundation
import Combine

/// Global application state shared via the Environment.
///
/// This class stores high level flags such as whether the user is
/// authenticated and whether Demo Mode is enabled.  Views observe
/// these published properties to update their presentation accordingly.
final class AppState: ObservableObject {
    @Published var isAuthenticated: Bool = false
    @Published var demoMode: Bool = true
    @Published var currentUserId: String = "demo_user"

    init() {
        // Defaults to Demo Mode; in a real app this could be loaded
        // from UserDefaults or a configuration file.
    }
}