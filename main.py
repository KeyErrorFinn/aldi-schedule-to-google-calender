from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from beautiful_date import *
import cv2
import numpy as np
import pytesseract
import os
import shutil
from dotenv import load_dotenv

# Load .env file
load_dotenv()

event_name = "Rachel Working"
google_email = os.getenv("EMAIL")

calendar = GoogleCalendar(google_email, credentials_path=".credentials/credentials.json")

def showCV2image(opencv_image):
    # Resize the image to fit on the screen
    screen_width = 1280  # Set your desired width
    screen_height = 720  # Set your desired height

    # Calculate the scale factor while maintaining the aspect ratio
    height, width = opencv_image.shape[:2]
    scale_factor = min(screen_width / width, screen_height / height)

    # Resize the image
    new_size = (int(width * scale_factor), int(height * scale_factor))
    resized_image = cv2.resize(opencv_image, new_size, interpolation=cv2.INTER_AREA)

    # Display the image using OpenCV
    cv2.imshow("Image", resized_image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

def extract_text_from_image(image):
    # Convert the image to grayscale (optional, but can improve OCR accuracy)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(gray_image)

    return text

month_map = {
            "Jan": Jan,
            "Feb": Feb,
            "Mar": Mar,
            "Apr": Apr,
            "May": May,
            "Jun": Jun,
            "Jul": Jul,
            "Aug": Aug,
            "Sep": Sept,
            "Oct": Oct,
            "Nov": Nov,
            "Dec": Dec
        }

def addGoogleEvent(day, month, start_time, end_time):
        day = int(day)
        month = month_map[month]
        currentYear = D.today().year

        start_date = (day/month/currentYear)[start_time[0]:start_time[1]]
        end_date = (day/month/currentYear)[end_time[0]:end_time[1]]

        print(start_date)
        print(end_date)

        work_event = list(calendar.get_events(time_min=start_date, time_max=end_date, query=event_name))
        if len(work_event) == 0:
            print("No events on day")
            event = Event(event_name,
                            color_id="1",
                            start=start_date,
                            end=end_date
                        )
            
            calendar.add_event(event)
            print("\nEVENT ADDED")
        else:
            print("Events found")
            for event in work_event:
                print(event)


scheduleImagesDir = os.path.join(os.getcwd(), "schedule_imgs")
images = []

for itemName in os.listdir(scheduleImagesDir):
    if os.path.isfile(os.path.join(scheduleImagesDir, itemName)) and (itemName.endswith(".jpg") or itemName.endswith(".png")):
        images.append(itemName)

for imageName in images:
    print(f"Image: {imageName}\n")
    image_path = f'schedule_imgs/{imageName}'
    image = cv2.imread(image_path)

    image_height, image_width = image.shape[0], image.shape[1]

    image = image[475:image_height-288, 66:image_width-66]
    # List of template images
    template_paths = [
        'day_colour_imgs/blue_day.png',
        'day_colour_imgs/red_day.png',
        'day_colour_imgs/red_day_2.png'
        # Add more template paths here as needed
    ]

    # Store all matches
    matches = []
    showCV2image(image)
    # cv2.imwrite("imagething.png", image)

    # Loop through each template
    for template_path in template_paths:
        template_image = cv2.imread(template_path)
        if template_image is None:
            print(f"Could not read template image: {template_path}")
            continue

        # Get dimensions of the template
        h, w, _ = template_image.shape

        # Perform template matching
        result = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF_NORMED)

        # Set a threshold for matches
        threshold = 0.7
        yloc, xloc = np.where(result >= threshold)

        # Loop through the matches and store their locations
        for index, (x, y) in enumerate(zip(xloc, yloc)):
            if index == 0:
                matches.append((x, y, template_path))
            else:
                if y > matches[-1][1] + 310:  # Ensure the matches are sufficiently spaced
                    matches.append((x, y, template_path))
        
        print(f"Retrieve matches for: {template_path}")

    print(f"\nMatch Locations: {matches}\n")

    # for x, y, _ in matches:
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imwrite("output_red_rectangles.jpg", image)

    date_and_times = []
    for (x, y, _) in matches:
        day_image = image[y:y+h, :]

        day_date_image = day_image[:, :x]
        day_date_text = extract_text_from_image(day_date_image).split('\n')[0]
        if day_date_text == "":
            continue
        if " " not in day_date_text:
            day_date_text = day_date_text[:3] + " " + day_date_text[3:]
        day_date_tuple = tuple(day_date_text.split(" "))

        day_time_image = day_image[:, x+w:]
        day_time_text = extract_text_from_image(day_time_image).split('\n')[1]
        day_time_ranges = tuple(day_time_text[:day_time_text.find(" (")].split(" - "))

        date_and_times.append((day_date_tuple, day_time_ranges))

    print(f"Dates and Times: {date_and_times}")

    for date_and_time in date_and_times:
        month = date_and_time[0][0]
        day = date_and_time[0][1]
        start_time = date_and_time[1][0]
        end_time = date_and_time[1][1]

        if start_time.startswith("0"):
            start_time = start_time[1:]

        if end_time.startswith("0"):
            end_time = end_time[1:]

        start_time = start_time.split(":")
        start_time = [int(start_time[0]), int(start_time[1])]
        end_time = end_time.split(":")
        end_time = [int(end_time[0]), int(end_time[1])]

        print(f"\nDate and Time: {day}; {month}; {start_time}; {end_time}")

        addGoogleEvent(day, month, start_time, end_time)
    
    shutil.copy2(image_path, 'schedule_imgs/added/')
    os.remove(image_path)


    # print("Match locations (top-left corners and templates):", matches)