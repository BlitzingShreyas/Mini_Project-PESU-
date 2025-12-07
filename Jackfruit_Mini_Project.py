import calendar

import datetime
import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


from datetime import date   
from dateutil.relativedelta import relativedelta


print("")
print("----****----****----****----****--WELCOME TO DAY AND TIME APPLICATIONS PROJECT--****---****----****----****----")
print("")

                                        #DAY OF THE WEEK CALCULATOR
def day_week_calc():
    #intializing the colours
    BLUE = "\033[34m"
    RESET = "\033[0m"

    str = input("Enter the date in DD/MM/YYYY format : ")
    #splitting the given string to days,months and year
    lst =str.split("/")

    cal = calendar.monthcalendar(int(lst[2]), int(lst[1]))

    print("")
    print("       ",end="")
    print(calendar.month_name[int(lst[1])], int(lst[2]))
    print("Mo  Tu  We  Th  Fr  Sa  Su")

    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day == int(lst[0]):
                    #highlighting the target date
                line += BLUE + f"{day:2d}" + RESET + " "
            else:
                line += f"{day:2d} "
                line += " "
        print(line)

    print("")
    print(f"The day on {str} was {calendar.day_name[calendar.weekday(int(lst[2]),int(lst[1]), int(lst[0]))]}")
    
                                        #EVENT COUNTDOWN TO A FUTURE EVENT

def event_countdown():
    
#Countdown Logic
    # define future_date in the enclosing scope so nested functions can modify it
    future_date = None

    def start_countdown():
        #inputting the event name and its date and time
        nonlocal future_date
        event_name = event_entry.get()
        date_str = date_entry.get()
        time_str = time_entry.get()
        
        #checking if the fields are filled or not
        if not event_name or not date_str or not time_str:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            event_datetime_str = date_str + " " + time_str
            #splitting the given input into the date and time format
            future_date = datetime.datetime.strptime(event_datetime_str, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            messagebox.showerror("Format Error", "Use formats:\nDate: DD/MM/YYYY\nTime: HH:MM:SS")
            return

        start_button.config(state="disabled")
        update_countdown(event_name)


    def update_countdown(event_name):

        #getting todays date
        now = datetime.datetime.now()
        if future_date is None:
            # nothing to update yet
            countdown_label.config(text="No event set")
            return

        time_left = future_date - now
        seconds_left = time_left.total_seconds()

        #checking if the date is already passed
        if seconds_left <= 0 and seconds_left > -1:
            countdown_label.config(text=f"🎉 IT'S TIME! {event_name}!")
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(r"/Users/shreyashegde/Downloads/031974_30-seconds-alarm-72117.mp3")
                pygame.mixer.music.play()
                root.after(10000, pygame.mixer.music.stop)
            except Exception:
                pass
            start_button.config(state="normal")
            return
        if seconds_left < 0:
            days_ago = abs(time_left.days)
            countdown_label.config(text=f"{event_name} was {days_ago} days ago!")
            return

        #calculating the remaining days , hours , minutes and seconds
        days = time_left.days
        seconds = time_left.seconds

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60

        #outputting the countdown
        countdown_label.config(
            text=f"{days:02d} days : {hours:02d} hrs : {minutes:02d} mins : {remaining_seconds:02d} secs"
        )

        root.after(1000, update_countdown, event_name)

    # GUI Layout 

    # Create the main root window (do not withdraw it) so the GUI reliably appears
    root = tk.Tk()
    root.title("Event Countdown Timer")
    root.geometry("1500x1200")

    # ---------- Background Image ----------
    try:
        bg_image = Image.open("/Users/shreyashegde/Documents/clock2.jpg")     # put your file name here
        bg_image = bg_image.resize((1800, 1700))      # resize to window
        bg_photo = ImageTk.PhotoImage(bg_image)
        root.bg_photo = bg_photo

        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        # If background image fails to load, continue without it
        pass
    # --------------------------------------


    title_label = tk.Label(root, text="EVENT COUNTDOWN TIMER", font=("Algerian", 60, "bold"),highlightcolor="white",bg="#d6824d")
    title_label.pack(pady=10)

    # Event Output
    tk.Label(root, text="Event Name:", font=("Verdana", 40), bg="#d6824d").pack()
    event_entry = tk.Entry(root, font=("Arial", 35), width=30,bg="#93e9d2")
    event_entry.pack(pady=5)

    # Date Field Box
    tk.Label(root, text="Event Date (DD/MM/YYYY):", font=("Verdana", 40), bg="#d6824d").pack()
    date_entry = tk.Entry(root, font=("Arial", 35), width=30,bg="#93e9d2")
    date_entry.pack(pady=5)

    # Time Field Box
    tk.Label(root, text="Event Time (HH:MM:SS):", font=("Verdana", 40), bg="#d6824d").pack()
    time_entry = tk.Entry(root, font=("Arial", 35), width=30,bg="#93e9d2")
    time_entry.pack(pady=5)

    # Start Button
    start_button = tk.Button(root, text="Start Countdown", font=("Verdana", 25), command=start_countdown)
    start_button.pack(pady=15)

    # Countdown Output
    countdown_label = tk.Label(root, text="**************", font=("Verdana", 30),bg="#e39e79")
    countdown_label.pack(pady=20)

    # handle window close to ensure pygame stops if playing
    def on_close():
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the Tk event loop so the window actually appears
    root.mainloop()

    

                                   #AGE CALCULATOR
                                         
def age_calculator():

    def calculate_detailed_age(birth_date, current_date):
        """
        Calculates the exact age in years, months, and days 
        using the relativedelta function.
        """
        # relativedelta provides the difference broken down into years, months, and days
        difference = relativedelta(current_date, birth_date)
        return difference.years, difference.months, difference.days

    def get_age_from_user_input_detailed():
        """
        Prompts the user for their birth date, calculates and prints 
        the age in years, months, and days, including error handling.
        """
        # Define the required date format
        DATE_FORMAT = "%d/%m/%Y"
        
        while True:
            # Prompt user for input
            birth_date_str = input("Please enter your birth date (in DD/MM/YYYY format, e.g., 25/12/1985): ")
            
            try:
                # Convert the string input to a date object
                birth_date = datetime.datetime.strptime(birth_date_str, DATE_FORMAT).date()
                
                # Check for a future date (simple exception concept)
                if birth_date > date.today():
                    raise ValueError("Birth date cannot be in the future.")
                
                break # Exit the loop if input is valid
                
            except ValueError as e:
                # Handle two types of errors: invalid format and future date
                if "Birth date cannot be in the future" in str(e):
                    print(f"*Error:* {e}")
                else:
                    print(f"*Error:* The date format must be {DATE_FORMAT} or the date is invalid. Please try again.")

        # Get the current date
        current_date = date.today()

        # Calculate the age breakdown
        years, months, days = calculate_detailed_age(birth_date, current_date)

        # Display the result
        print("" + "="*40)
        print(f"Your Birth Date: {birth_date.strftime(DATE_FORMAT)}")
        print(f"Today's Date: {current_date.strftime(DATE_FORMAT)}")
        print("-"*40)
        print(f"Your exact age is:")
        print(f"*{years}* years, *{months}* months, and *{days}* days.")
        print("="*40)

    # Execute the function to run the program
    get_age_from_user_input_detailed()


print("What would you like to execute:-->Day of the Week calculator	-->Countdown to a future event	-->Age Calculator")
print("Enter your choice based on the given menu\n1. Day of the week caulculator\n2. Countdown to a Future Event\n3. Age Calculator")
choice=int(input())
if choice == 1:
   day_week_calc()
elif choice == 2:
   event_countdown()
elif choice == 3:
    age_calculator()
else:
    print("Wrong Choice")
    print("Enter your choice based on the given menu\n1. Day of the week caulculator\n2. Countdown to a Future Event\n" \
    "3. Age Calculator")
    choice=int(input())
    if choice not in (1,2,3):
        print("Wrong Choice Again!!")
        print("Maximum Attempts Exceeded.")
        exit()
    else:
        if choice == 1:
            day_week_calc()
        elif choice == 2:
            event_countdown()
        elif choice == 3:
            age_calculator()
print("Do you wish to proceed-enter YES or NO")
choice2=input().lower()
if choice2=="yes":
    print("Enter your choice based on the given menu\n1. Day of the week caulculator\n2. Countdown to a Future Event\n" \
           "3. Age Calculator")
    choice=int(input())
    if choice == 1:
        day_week_calc()
    elif choice == 2:
        event_countdown()
    elif choice == 3:
        age_calculator()
    else:
        print("Wrong Choice!!")      
        print("Enter the right choice: ")
        choice=int(input())
        if choice not in (1,2,3):
            print("Wrong Choice Again!!")
            print("Maximum Attempts Exceeded.")
            exit()
        else:
            if choice == 1:
                day_week_calc()
            elif choice == 2:
                event_countdown()
            elif choice == 3:
                age_calculator()
else:
    print("THANKYOU FOR VISITING THIS PROJECT😊😊!!!")
