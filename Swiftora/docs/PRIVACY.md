# Privacy Notice for the Swiftora Demo

Swiftora respects your privacy.  The demo mode contained within this
repository is designed to run **entirely on your local machine**.  No
photos, notes, metadata or personal information are transmitted to
external services.  Please read the following points carefully:

1. **Local Processing Only.**  All image analysis, comparable
   selection and pricing occurs on your device using deterministic
   heuristics and locally shipped data.  There are no calls to remote
   machine learning or pricing services in Demo Mode.
2. **Fake Authentication.**  The login screen simply stores your
   provided email and password into local storage (UserDefaults) for
   demonstration purposes.  These credentials are not transmitted or
   validated against a server.
3. **Images Are Not Uploaded.**  When you select or capture a
   photograph it is compressed and stored in the app's sandbox on your
   device.  It is used only for the duration of the analysis and is
   not sent to any third party.
4. **Generated Data Persists Locally.**  The history of your
   generation jobs is written to a local SQLite database.  This file
   remains on your device until you delete the app.
5. **No Tracking or Analytics.**  The demo does not include any
   analytics libraries, crash reporters or other telemetry.  Your
   behaviour is not tracked.

When you choose to enable Live Mode in the future, data may be
transmitted to external services such as OpenAI, eBay and Firebase.
Refer to the privacy policies of those providers and the documentation
in `docs/switch_to_live.md` for details on how your data will be
handled.