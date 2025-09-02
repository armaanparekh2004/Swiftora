import SwiftUI

/// Root view that decides whether to show authentication or the main
/// application interface based on `AppState`.
struct ContentView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        if appState.isAuthenticated {
            MainTabView()
        } else {
            AuthView()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environmentObject(AppState())
    }
}