import SwiftUI

/// Screen for selecting an image and optional notes to send to the backend.
struct UploadView: View {
    @EnvironmentObject var appState: AppState
    @State private var showImagePicker = false
    @State private var selectedImage: UIImage?
    @State private var notes: String = ""
    @State private var isLoading = false
    @State private var job: UserJob?
    @State private var navigateToResult = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            VStack(spacing: 24) {
                if let img = selectedImage {
                    Image(uiImage: img)
                        .resizable()
                        .scaledToFit()
                        .frame(height: 200)
                        .cornerRadius(12)
                } else {
                    Rectangle()
                        .fill(Color.secondary.opacity(0.1))
                        .frame(height: 200)
                        .overlay(
                            Text("Tap to select photo")
                                .foregroundColor(.secondary)
                        )
                        .onTapGesture {
                            showImagePicker = true
                        }
                }

                TextField("Optional notes (e.g. 128GB)", text: $notes)
                    .padding()
                    .background(Color(uiColor: .secondarySystemBackground))
                    .cornerRadius(8)

                if let errorMessage = errorMessage {
                    Text(errorMessage)
                        .font(.footnote)
                        .foregroundColor(.red)
                }

                Button(action: generate) {
                    if isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle())
                            .frame(maxWidth: .infinity)
                            .padding()
                    } else {
                        Text("Generate")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                }
                .background((selectedImage == nil || isLoading) ? Color.gray : Color.primaryColor)
                .cornerRadius(8)
                .disabled(selectedImage == nil || isLoading)

                Spacer()
                NavigationLink(destination: GenerateView(job: job), isActive: $navigateToResult) {
                    EmptyView()
                }
            }
            .padding()
            .navigationTitle("Upload")
            .sheet(isPresented: $showImagePicker) {
                ImagePicker(sourceType: .photoLibrary) { image in
                    self.selectedImage = image
                }
            }
        }
    }

    private func generate() {
        guard let image = selectedImage else { return }
        isLoading = true
        errorMessage = nil
        APIService.shared.analyze(image: image, notes: notes.isEmpty ? nil : notes, userId: appState.currentUserId) { result in
            isLoading = false
            switch result {
            case .success(let job):
                self.job = job
                self.navigateToResult = true
            case .failure(let error):
                self.errorMessage = error.localizedDescription
            }
        }
    }
}

struct UploadView_Previews: PreviewProvider {
    static var previews: some View {
        UploadView().environmentObject(AppState())
    }
}