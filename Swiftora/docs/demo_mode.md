# Demo Mode

Swiftora launches in **Demo Mode** by default.  In this mode the entire
application – both frontend and backend – operates locally on your
machine.  No external network calls are made and no personal data
leaves your device.  Demo Mode is ideal for experimenting with the
workflow, performing development, and demonstrating the concept
without incurring any costs.

## What Demo Mode Does

* **Fake Authentication:** The login screen accepts any non‑empty
  email/password combination and stores it locally.  There is no
  remote user store in Demo Mode.
* **Local AI Pipeline:** When you upload an image the backend uses
  simple heuristics to parse the filename and compute basic image
  statistics.  These heuristics determine a category, brand, model,
  colour, approximate size and a pseudo‑random condition.  There is
  deliberately no machine learning model invoked.
* **Comparison Fixtures:** A CSV file (`backend/fixtures/comps_seed.csv`)
  ships with the repository containing 300+ rows of synthetic price
  comparisons across common categories like phones, shoes and cameras.
  The backend filters these rows using fuzzy matching on the detected
  brand/model and returns 8–12 comparable listings.
* **Robust Pricing:** The prices of the returned comparables are fed
  into a robust estimator which trims outliers (via Tukey fences),
  computes the 10th, 50th and 90th percentiles and derives a
  confidence score.  This results in a low/mid/high price band.
* **Templated Copy:** Using the detected attributes and price band the
  backend builds a human readable title and bullet point list.  These
  strings are deterministic so that the same input always yields the
  same output.
* **Local Storage:** Every generation job is written to a local SQLite
  database using GRDB.  The History tab can be expanded to read
  from this database.

## Running Demo Mode

1. Install the Python dependencies and start the backend server:

   ```bash
   cd backend
   pip install -r requirements.txt
   make run
   ```

2. Open the iOS project in Xcode and run it on a simulator.  Ensure
   that the backend is running locally on `localhost:8000`.

3. Log in with any credentials, select a photo (or use one of the
   images under `sample_images/`), optionally add notes, and tap
   **Generate**.  Within a second you will see the detected
   attributes, comparable listings, price range and templated copy.

4. Use the **Copy** buttons to place the generated title/description
   on the clipboard or **Share** to bring up the iOS share sheet.  No
   network requests occur.

## Limitations

* Demo Mode does not call any external APIs.  Therefore the
  heuristics and fixtures are intentionally simplistic and may not
  reflect real world data.
* Live Mode (using OpenAI, eBay Browse, Firebase, etc.) is scaffolded
  but disabled.  See `docs/switch_to_live.md` for activation steps.
* The History screen currently displays a placeholder message.  The
  underlying database is created but a data access layer has not
  yet been implemented.
