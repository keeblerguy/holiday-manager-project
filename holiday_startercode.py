from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass, field
from config import weather_key
from config import json_loc
from config import current_year
from config import scraped
from config import config_loc


@dataclass
class Holiday:
    name: str
    date: datetime

    def get_weather_forecast (self,  zip):
        response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?zip={zip},us&appid={weather_key}')

        for node in json.loads(response.text)['list']:
            if datetime.strptime(self.date, '%Y-%m-%d').date() == datetime.fromtimestamp(node['dt']).date():
                return node['weather'][0]['description']

        return 'No weather data.'
      
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    innerHolidays: list = field(default_factory= list)

    def add_holiday(self, holiday):
        self.innerHolidays.append(holiday)

    def find_holiday(self, name, year):
        if year != False:
            return any(holiday.name == name and str(datetime.strptime(holiday.date, '%Y-%m-%d').year) == year for holiday in self.innerHolidays)

        else:
            return any(holiday.name == name for holiday in self.innerHolidays)
        # Find Holiday in innerHolidays
        # Return Holiday

    def remove_holiday(self, name, year):
        if year == 'ALL':
            self.innerHolidays = list(filter(lambda holiday: holiday.name != name, self.innerHolidays))

        else:
            self.innerHolidays = list(filter(lambda holiday: holiday.name != name or str(datetime.strptime(holiday.date, '%Y-%m-%d').year) != year, self.innerHolidays))

        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self):
        file = open(json_loc)

        for holiday in json.load(file)['holidays']:
            self.innerHolidays.append(Holiday(holiday['name'], holiday['date']))

        file.close()
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self):
        holidays = {'holidays':[]}
        
        for holiday in self.innerHolidays:
            holidays['holidays'].append({'name':holiday.name, 'date':holiday.date})

        file = open(json_loc,'w')

        json.dump(holidays, file)

        file.close()
        # Write out json file to selected file.

    def filterHolidaysByWeek(self,year, week):
        if week == "CURRENT":
            return list(filter(lambda holiday: str(datetime.strptime(holiday.date, '%Y-%m-%d').year) == year and str(datetime.strptime(holiday.date, '%Y-%m-%d').strftime('%V')) == datetime.now().strftime('%V'), self.innerHolidays))

        else:
            if len(week) == 1:
                week = f'0{week}'

            return list(filter(lambda holiday: str(datetime.strptime(holiday.date, '%Y-%m-%d').year) == year and str(datetime.strptime(holiday.date, '%Y-%m-%d').strftime('%V')) == datetime.now().strftime('%V'), self.innerHolidays))
        
    

def scrape_holidays(holidayList):
    for year in range(current_year - 2, current_year + 2):
        response = requests.get(f'https://www.timeanddate.com/holidays/us/{year}')
        tbody = BeautifulSoup(response.text, 'html.parser').find('table', attrs = {'id':'holidays-table'}).find('tbody')

        for row in tbody.find_all('tr'):
            if len(row.find_all()) !=0:
                date =datetime.strftime(datetime.strptime(f'{row.th.string} {year}', '%b %d %Y'), '%Y-%m-%d')
                name = row.select_one('td > a').string

                holidayList.addHoliday(Holiday(name, date))
        
        print('Scraping successful.')
        print('')
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     
def welcome_message(holiday_count):
    print('Holiday Manager')
    print('===============')
    print(f'There are {holiday_count} holidays stored in the system.')
    print('')

def menu():
    print('Menu')
    print('=====')
    print('1 - Add a Holiday')
    print('2 - Remove a Holiday')
    print('3 - Save Holiday List')
    print('4 - View Holidays')
    print('5 - Exit')
   
def main():
    holidayList = HolidayList()

    holidayList.read_json()

    if not scraped:
        scrape_holidays(holidayList)

        holidayList.save_to_json()

        file = open(config_loc, 'r')
        file.seek(16)
        lines = file.readlines()
        lines.insert(0, 'scraped = True')

        file = open(config_loc, 'w')
        file.write(''.join(lines))

    welcome_message(len(holidayList.innerHolidays))

    user_exited = False

    while not user_exited:
        menu()

        menu_choice = input('')

        if menu_choice == '1':
            print('')
            print('Add a Holiday')
            print('==============')

            valid_name = False
            while not valid_name:
                name = input('Holiday: ')

                if len(name) != 1:
                    valid_name = True

                else: 
                    print('Holiday name is too short.')
                    print('')

            valid_date = False
            while not valid_date:
                date = input('Date [YYYY-MM-DD]: ')

                try:
                    datetime.strptime(date, '%Y-%m-%d')

                    if int(date[0:4]) > 1500 and int(date[0:4]) < 2500:

                        holiday = Holiday(name, date)

                        if holiday not in holidayList.innerHolidays:
                            holidayList.add_holiday(holiday)

                            print('')
                            print(f'{name} ({date}) has been successfully added.')
                            print('')

                            valid_date = True
                        else:
                            print('')
                            print('Holiday already exists')
                            print('')

                            valid_date = True
                    else:
                        print('Year out of range.')
                        print('')
                
                except ValueError:
                    print('Incorrect date format.')
                    print('')

        elif menu_choice == '2':
            print('')
            print('Remove a Holiday')
            print('=================')

            valid_year = False
            while not valid_year:
                year = input("Year (type 'all' to remove all instances): ")

                if year.upper() == 'ALL':
                    valid_year = True
                
                elif year.isnumeric():
                    if int(year) > 1500 and int(year) < 2500:
                        valid_year = True

                    else:
                        print('Year out of range.')

                else:
                    print('Invalid year.')

            valid_name = False
            while not valid_name:
                name = input('Holiday: ')

                if year.upper() == 'ALL':

                    if holidayList.find_holiday(name, False):
                        holidayList.remove_holiday(name, year.upper())
                        print('')
                        print(f'{name} has been successfully removed.')
                        print('')
                        valid_name = True
                    else:
                        print('Holiday could not be found.')

                else:

                    if holidayList.find_holiday(name, year):
                        holidayList.remove_holiday(name, year)
                        print('')
                        print(f'{name} has been successfully removed.')
                        print('')
                        valid_name = True

                    else:
                        print('Holiday could not be found.')

        elif menu_choice == '3':
            print('')
            print('Save Holiday List')
            print('===============')

            valid_choice = False
            while not valid_choice:
                choice = input('Are you sure you want to save your changes? [y/n]: ').lower()

                if choice == 'y':
                    holidayList.save_to_json()
                    print('')
                    print('File successfully saved.')
                    print('')
                    valid_choice = True

                elif choice == 'n':
                    print('')
                    print('File was not saved.')
                    valid_choice = True
                
                else:
                    print('Please enter a valid input.')

        elif menu_choice == '4':
            print('')
            print('View Holidays')
            print('===============')

            valid_year = False
            while not valid_year:
                year = input('Year: ')

                if year.isnumeric():
                    if int(year) > 1500 and int(year) < 2500:
                        valid_year = True

                    else:
                        print('Year is out of range.')

                else:
                    print('Invalid year')

            valid_week = False
            while not valid_week:
                if year == str(current_year):
                    week = input("Week [1-52 or type 'current' to view current week]: ")

                else:
                    week = input("Week [1-52]: ")
                
                if week.isnumeric():
                    if int(week) >= 1 and int(week) <= 52:
                        print('')
                        valid_week = True

                    else:
                        print('Week out of range.')

                elif week.upper() == "CURRENT" and year == str(current_year):
                    valid_choice = False
                    while not valid_choice:
                        weather_choice = input('Display weather [y/n]?: ').lower()

                        if weather_choice == 'y':
                            valid_zip = False
                            while not valid_zip:
                                zip = input('Zip code: ')

                                if zip.isnumeric() and len(zip) == 5:
                                    print('')
                                    valid_zip = True

                                else:
                                    print('Please enter a valid zip code.')

                            valid_choice = True

                        elif weather_choice == 'n':
                            valid_choice = True

                        else:
                            print('Please input a valid choice.')

                    valid_week = True
                
                else:
                    print('Invalid week.')

            holidays_by_week = holidayList.filterHolidaysByWeek(year, week.upper())

            if len(holidays_by_week) == 0:
                print(f'Holidays for {year}, Week {week}.')
                print('==============================')
                print('No holidays occur during this week.')
                print('')

            elif week.upper() == 'CURRENT' and weather_choice == 'y':
                print('Holidays and weather for the Current Week')
                print('===================================')
                
                for holiday in holidays_by_week:
                    print(f'{holiday.name} ({holiday.date} - {holiday.get_weather_forecast(zip)}')

                print('')
            
            else:
                print(f'Holidays for {year}, Week {week}.')
                print('===========================')

                for holiday in holidays_by_week:
                    print(f'{holiday.name} ({holiday.date})')

                print('')

        elif menu_choice == '5':
            temp_holiday_list = HolidayList()

            temp_holiday_list.read_json()

            if temp_holiday_list.innerHolidays != holidayList.innerHolidays:
                changes = True

            else:
                changes = False

            valid_choice = False
            while not valid_choice:
                print('')

                if changes:
                    print('You have unsaved changes.')

                ask = input('Are you sure you want to exit? [y/n]: ').lower()

                if ask == 'y':
                    print('')
                    print('Good bye!')
                    user_exited = True
                    valid_choice = True

                elif ask == 'n':
                    print('')
                    valid_choice = True

                else:
                    print('Please input a valid choice.')
        
        else:
            print('Please enter a valid choice.')
 

if __name__ == "__main__":
    main();







