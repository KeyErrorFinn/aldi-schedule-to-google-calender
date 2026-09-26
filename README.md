# ALDI Schedule to Google Calendar

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" />
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=fff" />
  <img alt="Tesseract OCR" src="https://img.shields.io/badge/Tesseract%20OCR-4285F4?logo=google&logoColor=fff" />
  <img alt="Google Calendar" src="https://img.shields.io/badge/Google%20Calendar-4285F4?logo=googlecalendar&logoColor=fff" />
</p>

A personal Python tool that reads mobile screenshots from the ALDI scheduling app and creates matching Google Calendar events.

> [!WARNING]
> The crop coordinates, colour templates, spacing, and OCR assumptions match one specific mobile layout. A changed app layout, different screen size, or poor screenshot can produce incorrect dates and times.

## What it does

1. Reads `.jpg` and `.png` files from `schedule_imgs/`.
2. Crops the known schedule area.
3. Finds red and blue work-day markers with OpenCV template matching.
4. Uses Tesseract to read each date and shift time.
5. Checks the selected Google Calendar for a matching `Work Shift` event.
6. Creates missing events.
7. Moves each examined screenshot into `schedule_imgs/added/`.

The script uses the current year. It does not currently handle schedules that cross into another year.

## Requirements

- Python 3
- Tesseract OCR installed and available to `pytesseract`
- A Google account
- Google Calendar API desktop OAuth credentials
- The packages in `requirements.txt`

~~~bash
python -m pip install -r requirements.txt
~~~

## Setup

1. Copy `.env.example` to `.env` and enter the calendar account:

   ~~~dotenv
   EMAIL=account@example.com
   ~~~

2. Save the Google OAuth desktop client file as:

   ~~~text
   .credentials/credentials.json
   ~~~

3. Create both processing directories:

   ~~~text
   schedule_imgs/
   schedule_imgs/added/
   ~~~

4. Put schedule screenshots into `schedule_imgs/`.
5. Keep `day_colour_imgs/` beside `main.py`.
6. Review `event_name` near the top of `main.py` if you want a different calendar title.

Never commit `.env`, OAuth credentials, generated tokens, or private schedule screenshots.

## Run

~~~bash
python main.py
~~~

Windows users can also run `Run.bat`.

The first Google Calendar connection may open an OAuth authorisation flow. Review the requested account and permissions before approving it.

## Important behaviour

- Duplicate checks use the event name and the extracted time range.
- Calendar events use colour ID `1`.
- The screenshot is moved after the script finishes examining it, even when no shift was recognised. Check `schedule_imgs/added/` and the console output when an event is missing.
- Start and end times are created on the same date. Overnight shifts are not handled specially.
- OCR output is not validated before calendar creation.

## Troubleshooting

| Problem | Check |
| --- | --- |
| `schedule_imgs` error | Create both required directories before running. |
| No work days found | Confirm the screenshot matches the expected mobile layout and that `day_colour_imgs/` is present. |
| Tesseract is not found | Install Tesseract and make sure `pytesseract` can locate the executable. |
| Google authentication fails | Confirm the email and `.credentials/credentials.json` belong to the same intended Google account. |
| Wrong event date or time | Inspect the printed `Dates and Times` output before trusting the created event. |

## Project files

- `main.py`, image detection, OCR, calendar lookup, and event creation.
- `day_colour_imgs/`, templates used to identify working days.
- `.env.example`, calendar account configuration template.
- `Run.bat`, Windows shortcut.
- `requirements.txt`, pinned Python packages.

## Licence

No project-level licence is currently included. Third-party packages and Google services keep their own terms and licences.
