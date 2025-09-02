import SwiftUI

/// Authentication screen for Demo Mode.  This view performs a fake
/// authentication by simply storing the email and password into
/// UserDefaults.  Any non‑empty email/password combination will
/// succeed.  The `Login` button writes the credentials and flips
/// `AppState.isAuthenticated` to true.
struct AuthView: View {
    @EnvironmentObject var appState: AppState
    @State private var email: String = ""
    @State private var password: String = ""
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            VStack(spacing: 24) {
                Text("Welcome to Swiftora")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.primaryColor)

                TextField("Email", text: $email)
                    .keyboardType(.emailAddress)
                    .textContentType(.username)
                    .autocapitalization(.none)
                    .padding()
                    .background(Color(uiColor: .secondarySystemBackground))
                    .cornerRadius(8)

                SecureField("Password", text: $password)
                    .textContentType(.password)
                    .padding()
                    .background(Color(uiColor: .secondarySystemBackground))
                    .cornerRadius(8)

                if let errorMessage = errorMessage {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .font(.footnote)
                }

                Button(action: login) {
                    Text("Login")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.primaryColor)
                        .cornerRadius(8)
                }
                .disabled(email.isEmpty || password.isEmpty)

                Spacer()
            }
            .padding()
            .navigationBarHidden(true)
        }
    }

    private func login() {
        guard !email.isEmpty, !password.isEmpty else {
            errorMessage = "Please enter email and password."
            return
        }
        // Store credentials to UserDefaults for demo purposes
        UserDefaults.standard.set(email, forKey: "swiftora_email")
        UserDefaults.standard.set(password, forKey: "swiftora_password")
        appState.isAuthenticated = true
        appState.currentUserId = email
    }
}

struct AuthView_Previews: PreviewProvider {
    static var previews: some View {
        AuthView().environmentObject(AppState())
    }
}