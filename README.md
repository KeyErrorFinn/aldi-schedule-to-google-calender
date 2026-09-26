# ALDI Schedule to Google Calendar

A Python image-processing tool that reads mobile screenshots from the ALDI scheduling app and creates matching events in Google Calendar.

> [!WARNING]
> The crop coordinates, colour templates, spacing, and OCR assumptions are tailored to a specific mobile screenshot layout. Desktop screenshots and changed app layouts are likely to fail.

## Processing flow

1. Load `.jpg` and `.png` files from `schedule_imgs/`.
2. Crop the known schedule region.
3. Locate red and blue work-day markers using OpenCV template matching.
4. Divide the screenshot into matching day sections.
5. Use Tesseract OCR to extract the date and shift times.
6. Check Google Calendar for an existing event with the configured name and time.
7. Create missing events and move processed screenshots into `schedule_imgs/added/`.

## Requirements

- Python 3
- Tesseract OCR installed and available to `pytesseract`
- A Google account and Calendar API OAuth desktop credentials
- The packages in `requirements.txt`

```bash
python -m pip install -r requirements.txt
```

## Setup

1. Copy `.env.example` to `.env` and set the target calendar account:

   ```dotenv
   EMAIL=account@example.com
   ```

2. Put the Google OAuth client credentials at:

   ```text
   .credentials/credentials.json
   ```

3. Create `schedule_imgs/` and place the mobile schedule screenshots inside it.
4. Review `event_name` near the top of `main.py`; it is currently set directly in the source.
5. Keep `day_colour_imgs/` beside the script.

Never commit the populated credentials file, OAuth tokens, private schedule screenshots, or the populated `.env`.

## Running

```bash
python main.py
```

On Windows, `Run.bat` provides a shortcut.

## Important behaviour

- The current year is applied to recognised dates.
- Existing events are checked by time range and `event_name` to reduce duplicates.
- Successfully processed source images are moved, not copied.
- OCR and template matching can be wrong. Review created events before relying on them.
