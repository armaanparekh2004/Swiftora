# Swiftora

Swiftora is an offline-first mobile application demo that lets you photograph an item and receive a suggested title, description and price range without ever leaving your device.  The companion FastAPI backend performs lightweight analysis using deterministic heuristics and never touches the public internet while Demo Mode is enabled.

This repository is intentionally monorepo‑style.  The root contains two primary folders:

* **`backend/`** – A small FastAPI service that exposes the endpoints used by the mobile app.  In Demo Mode it loads pricing and comparison data from local CSV fixtures, runs a robust price estimate and builds copy using deterministic templates.  All tests for the pricing logic live under `backend/tests/`.
* **`ios/`** – A SwiftUI application which communicates exclusively with the local backend when `DEMO_MODE` is enabled.  It contains screens for fake authentication, photo upload, generation of AI‑like results, history of previous jobs and settings.  The iOS client persists all generated `UserJob` objects to a local SQLite database via [GRDB](https://github.com/groue/GRDB.swift).

## Getting Started

### Prerequisites

The demo has been designed to run completely offline.  You do **not** need to sign into an Apple Developer account or provide any API keys to build and test the app on the iOS Simulator.  You will need the following tools installed locally:

* Python 3.9+ and `pip` to run the backend.  The dependencies are listed in `backend/requirements.txt`.
* [Xcode](https://developer.apple.com/xcode/) (version 14 or newer) to build and run the SwiftUI application in the iOS Simulator.  No paid developer account is required for simulator builds.

### Running the Backend

1. From the project root, change into the backend directory:

   ```bash
   cd backend
   ```

2. Install the Python dependencies (preferably in a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server on `localhost:8000`:

   ```bash
   make run
   ```

   The service exposes the following endpoints:

   * `GET /healthz` – Returns `{"status": "OK"}` for health checks.
   * `GET /comps?q=<query>` – Returns price comparison data filtered by an optional search query.
   * `POST /analyze` – Accepts an image file and optional notes.  Returns a fully populated `UserJob` JSON document based on local heuristics and fixtures.

4. Run the backend test suite with:

   ```bash
   make test
   ```

### Running the iOS Application

1. Open the Xcode workspace by double‑clicking `ios/Swiftora.xcodeproj` or opening the `Package.swift` in Xcode.  The project targets iOS 15 or later.
2. Ensure the backend is running locally (see previous section).
3. Build and run the **Swiftora** app on an iPhone 15 Pro simulator.  Upon launch you will be greeted with a login screen.  Since authentication is faked in Demo Mode, any email and password will succeed and be stored securely in the Keychain.
4. Upload a picture (try any file under `sample_images/` such as `iphone12_blue.jpg`), optionally enter notes, and generate the results.  You should see a detected category, a list of comparable listings, a suggested price range and templated title/description.  Use the **Copy** buttons to place text on the clipboard or **Share** to invoke the iOS share sheet.
5. The history tab lists all previously generated jobs stored in a local SQLite database.
6. Settings allows toggling Demo/Live mode.  Live mode is disabled in this demo but will be enabled once you add the appropriate API keys and flip the flag.

### Repository Structure

```text
Swiftora/
├── LICENSE                     MIT license for the project
├── README.md                  This file
├── .env.example               Example environment configuration
├── .editorconfig              Editor configuration for consistent style
├── .gitignore                 Ignore patterns for git
├── backend/                   FastAPI backend service
│   ├── main.py                FastAPI application entry point
│   ├── config.py              Configuration and environment loading
│   ├── utils.py               Helper functions for detection and copy generation
│   ├── pricing.py             Robust pricing functions
│   ├── requirements.txt       Python dependencies
│   ├── Makefile               Convenience commands (run, test, lint)
│   ├── fixtures/              Seed data used in Demo Mode
│   │   └── comps_seed.csv     Price and comparison fixture data (generated)
│   └── tests/                 Backend test suite
├── ios/                       SwiftUI client application
│   ├── Package.swift          Swift Package manifest for the app
│   ├── Sources/               Swift source files for the app and tests
│   │   ├── SwiftoraApp.swift  Main app declaration
│   │   ├── Models/            Data models shared across the app
│   │   ├── ViewModels/        Observable object classes and controllers
│   │   ├── Views/             SwiftUI screens for Auth, Upload, Generate, History and Settings
│   │   └── Resources/         Color definitions and asset catalog placeholders
│   ├── Tests/                 Xcode unit and UI tests
│   └── AppStoreAssets/        Placeholder screenshots and icons for distribution
├── sample_images/             Example images used during the demo
└── docs/                      Project documentation and demo artefacts
    ├── demo_mode.md          How to run and understand Demo Mode
    ├── switch_to_live.md     Steps to enable Live Mode with real API keys
    ├── PRIVACY.md            Privacy considerations for the demo
    ├── TERMS.md              Terms of use for the demo
    └── demo/                 Captured simulator run through of the app
        └── demo_run.mp4
```

## Demo and Live Modes

Swiftora ships with **Demo Mode** enabled by default.  In this mode the app and backend will only ever read or write data locally – nothing is uploaded to a remote server.  When you are ready to enable Live Mode, drop your API keys into your environment (see `.env.example`) and follow the instructions in `docs/switch_to_live.md` to connect the app to real vision and pricing services.

## Contributing

We welcome pull requests!  Please open an issue or draft pull request describing your changes.  A simple PR template lives under `.github/` to help you structure your contribution.

## License

This project is licensed under the terms of the MIT License.  See the [LICENSE](LICENSE) file for details.