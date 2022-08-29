# holiday-manager-project
## Explanation
This project uses data from [Time and Dates](https://www.timeanddate.com/holidays/us/) using Holidays in the USA and [Open Weather](https://openweathermap.org/api).
The purpose was to web scrape data from these websites in order to make a Holiday Manager application where users can recall the stored holidays, add new holidays, and be able to delete them.  A user can also check on weather within the application.
The application uses a config.py file which has been exlcuded from this GitHub.
In order to utilize it how I did within the code, create a config.py file like this:
```
weather_key = ""
json_loc = ""
current_year = 
scraped = ""
config_loc = ""
```
The weather key is an API key you get by creating an account on the Open Weather website.
The JSON location refers to the holiday.JSON file and the Config location refers to the output.JSON file.
The current year is the year that you decide to utilize this project.

The Jupyter Notebook that is included was where I tested the code to ensure that it was working.
