# Switching to Live Mode

While Swiftora is designed to function entirely offline in Demo Mode,
the architecture anticipates that you may later want to plug in real
services for vision and pricing.  Live Mode enables those remote
services.  This document outlines the steps required to flip the
switch.

## 1. Obtain API Keys

You will need accounts and keys for each external service that you
intend to use:

* **OpenAI API Key** – required if you want to leverage GPT‑powered
  vision or language models.
* **eBay Client ID / Client Secret** – for fetching real comparable
  listings via the [eBay Browse API](https://developer.ebay.com/api-docs/buy/browse/overview.html).
* **Firebase API Key & Project Details** – if you wish to use
  Firebase Authentication, Firestore or Storage for real user accounts
  and data persistence.

Sign up with these providers and record your keys in a secure
location.  Never commit secrets directly into source control.

## 2. Configure Environment Variables

Copy `.env.example` to `.env` and populate it with your keys:

```env
DEMO_MODE=false
OPENAI_API_KEY=sk-...
EBAY_CLIENT_ID=YOUR_EBAY_CLIENT_ID
EBAY_CLIENT_SECRET=YOUR_EBAY_CLIENT_SECRET
FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
```

Ensure `.env` is listed in `.gitignore` so that it is never
accidentally pushed.

## 3. Backend Changes

The backend reads `DEMO_MODE` from the environment via
`swiftora.backend.config.Settings`.  When `DEMO_MODE=false` the
/analyze endpoint should be modified to call your real services.

* **Vision Service** – Replace the call to `detect_attributes` with a
  call into your vision API (e.g. OpenAI's GPT‑4V) to extract
  structured attributes from the image.  Make sure to handle errors
  and timeouts gracefully.
* **Comps Service** – Replace the fixture filter in
  `filter_comps` with a request to eBay's Browse API.  Use the
  search term built from the detected brand/model and parse the
  returned listings into the required comp structure.  You can reuse
  the robust pricing logic from Demo Mode.
* **Auth & Storage** – Add routes for user sign up/login and
  persist jobs to your database (e.g. Firestore) instead of local
  SQLite.

Unit tests should be updated or expanded to cover the new paths.

## 4. iOS Changes

* **APIService Base URL** – Update `baseURL` in
  `APIService.swift` to point at your hosted backend (e.g.
  `https://api.swiftora.com`).
* **Demo Mode Toggle** – Remove the disabled state from the toggle in
  `SettingsView` so that users can switch between modes at runtime.
* **Authentication** – Replace the fake `AuthView` with real
  authentication screens that talk to Firebase Auth (or another
  provider).  Securely store the resulting auth token.
* **History** – Implement a data access layer using GRDB or an
  alternative to sync generated jobs from your backend.

## 5. Deployment Considerations

* **Apple Developer Program** – To run Swiftora on a physical device
  or distribute it via TestFlight/App Store you must enroll in the
  Apple Developer Program (US $99 per year).  The iOS Simulator
  remains free.
* **CI/CD** – Extend the provided GitHub Actions workflow to run
  integration tests, build and sign the app, and deploy to TestFlight.

By following these steps you can transition Swiftora from a local
prototype to a production‑ready application backed by real AI and
market data.