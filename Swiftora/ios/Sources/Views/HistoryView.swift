import SwiftUI

/// Displays a list of previously generated jobs stored in the local
/// SQLite database.  For this demo the implementation is a stub and
/// simply shows a placeholder message.  When switching to Live Mode
/// this view can be wired up to a GRDB database.
struct HistoryView: View {
    var body: some View {
        NavigationView {
            VStack {
                Text("History")
                    .font(.largeTitle)
                    .padding()
                Text("No history available in this demo.")
                    .foregroundColor(.secondary)
            }
        }
    }
}

struct HistoryView_Previews: PreviewProvider {
    static var previews: some View {
        HistoryView()
    }
}