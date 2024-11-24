<h1 align="center">
  Aldi Schedule to Google Calender Program
</h1>

<p align="center">
  <a href="https://github.com/KeyErrorFinn/aldi-schedule-to-google-calender/commits/main/"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/KeyErrorFinn/aldi-schedule-to-google-calender" /></a>
  <a href="https://github.com/KeyErrorFinn/aldi-schedule-to-google-calender/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/KeyErrorFinn/aldi-schedule-to-google-calender" /></a>
</p>
<p align="center">
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" /></a>
</p>


This project is for using screenshots of ALDI work schedules to add the work day and times to a Google Calendar for easier time management.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [How the program works](#how-the-program-works)
  - [TO-DO](#to-do)

## About the Project
> [!WARNING]
> The program only works with mobile screenshots of the schedule through the ALDI app. Desktop screenshots will fail.

The project uses python to add the ALDI work dates and times to a Google Calender.

The files also include a Batch file for easier running when used.

### How the program works:
1) Uses a google account email from `.env` file and a `credentials.json` from the `.credentials/` folder to connect to your Google Calendar
2) Goes through each image of a weeks schedule in the `schedule_imgs/` folder
3) Finds what days are being worked on by seeing if it has a red vertical line or a blue vertical line
4) Seperates the schedule into those days and gathers the day from the left and the time from the right
5) Uses a predefined variable for the name of the event, and then uses the day, start time, and end time to add the event to the Google Calander
6) Once done with all days in the image, it moves the image of the week's schedule into an `added/` folder

### TO-DO:
- [x] <s>Create Program</s>
- [x] <s>Adjust for longer days</s>
- [ ] Make it more versalite by using any image instead of just mobile
