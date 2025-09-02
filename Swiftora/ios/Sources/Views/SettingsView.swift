import SwiftUI

/// Displays settings for the application.  A toggle controls whether
/// Demo Mode is active.  In this demo Live Mode is disabled and the
/// toggle cannot be turned off.  The explanation text directs
/// developers to the documentation for enabling Live Mode later.
struct SettingsView: View {
    @EnvironmentObject var appState: AppState
    @State private var showLiveModeAlert = false

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Mode")) {
                    Toggle(isOn: $appState.demoMode) {
                        Text("Demo Mode")
                    }
                    .disabled(true)
                    .onTapGesture {
                        // Show explanation when user tries to toggle
                        showLiveModeAlert = true
                    }
                    Text("Demo mode cannot be turned off in this build.  See docs/switch_to_live.md for details.")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                }

                Section(header: Text("About")) {
                    Text("Version 0.0.1")
                    Text("© 2025 Swiftora")
                }
            }
            .navigationTitle("Settings")
            .alert(isPresented: $showLiveModeAlert) {
                Alert(title: Text("Live Mode Disabled"), message: Text("To enable live mode you'll need to supply API keys.  See docs/switch_to_live.md for full instructions."), dismissButton: .default(Text("OK")))
            }
        }
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView().environmentObject(AppState())
    }
}