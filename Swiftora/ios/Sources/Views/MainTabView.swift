import SwiftUI

/// Main tab view presented once the user is authenticated.
struct MainTabView: View {
    var body: some View {
        TabView {
            UploadView()
                .tabItem {
                    Label("Upload", systemImage: "camera")
                }
            HistoryView()
                .tabItem {
                    Label("History", systemImage: "clock")
                }
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
        }
    }
}

struct MainTabView_Previews: PreviewProvider {
    static var previews: some View {
        MainTabView()
    }
}