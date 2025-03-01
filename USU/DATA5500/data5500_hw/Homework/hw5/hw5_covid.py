# importing needed libaries
import requests # type: ignore
import json
from datetime import datetime

# file the list of states and terrritories is saved
fil_path = r"C:/Users/arika/USU/DATA5500/data5500_hw/Homework/hw5/states_territories.txt"

# creating a list of the states and territores
states = [line.strip() for line in open(fil_path).readlines()]

# list that has the state abbreviations from my file, and they're full spellings
state_names = {
    'al': 'Alabama', 'ak': 'Alaska', 'as': 'American Samoa', 'az': 'Arizona', 'ar': 'Arkansas', 
    'ca': 'California', 'co': 'Colorado', 'ct': 'Connecticut', 'dc': 'Washington DC', 'de': 'Delaware', 
    'fl': 'Florida', 'ga': 'Georgia', 'gu': 'Guam', 'hi': 'Hawaii', 'id': 'Idaho', 
    'il': 'Illinois', 'in': 'Indiana', 'ia': 'Iowa', 'ks': 'Kansas', 
    'ky': 'Kentucky', 'la': 'Louisiana', 'me': 'Maine', 'md': 'Maryland', 
    'ma': 'Massachusetts', 'mi': 'Michigan', 'mn': 'Minnesota', 'ms': 'Mississippi', 
    'mo': 'Missouri', 'mp': 'Northern Mariana Islands', 'mt': 'Montana', 'ne': 'Nebraska', 'nv': 'Nevada', 
    'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico', 'ny': 'New York', 
    'nc': 'North Carolina', 'nd': 'North Dakota', 'oh': 'Ohio', 'ok': 'Oklahoma', 
    'or': 'Oregon', 'pa': 'Pennsylvania', 'pr': 'Puerto Rico', 'ri': 'Rhode Island', 'sc': 'South Carolina', 
    'sd': 'South Dakota', 'tn': 'Tennessee', 'tx': 'Texas', 'ut': 'Utah', 
    'vt': 'Vermont', 'va': 'Virginia', 'vi': 'Virgin Islands', 'wa': 'Washington', 'wv': 'West Virginia', 
    'wi': 'Wisconsin', 'wy': 'Wyoming'
}

# function that takes abbreviation and gives full name and header
def print_state_name(state):
    full_name = state_names.get(state, 'Unknown abbreviation')
    
    # line between each state output
    print()

    # bolded state name and description of data
    print(f"\033[1m{full_name}\033[0m - Covid confirmed cases statistics")

    # line to seperate header from data
    print("----------------------------------------------------")

# average number of new daily confirmed cases
def average_new_cases(state_dct, new_case_key):
    
    # list of the cases for each day
    total_cases = [entry[new_case_key] for entry in state_dct]

    # calculating average
    average = round(sum(total_cases)/ len(total_cases),2)

    # printed output
    print("Average number of new daily confirmed cases: ", average)

# date with the highest new number of covid cases
def highest_new_cases(state_dct, new_case_key, date_key):

    # pulling the row with the highest cases from the dictionary
    max_cases = max(state_dct, key=lambda x: x[new_case_key])

    # pulling the number of cases from the highest row
    max_new_cases = max_cases['positiveIncrease']

    # formatting date
    highest_day = datetime.strptime(str(max_cases[date_key]), '%Y%m%d').strftime('%m/%d/%Y')

    # printed output
    print(highest_day + " had the most new cases of " + str(max_new_cases) + ".")
 
# Most recent date with no new covid cases 
def date_no_cases(state_dct, new_case_key, date_key):

    # key for latest date 
    latest_date = None

    # going through each day, if new cases - 0 add to the date lsit
    for day in state_dct:
        if day[new_case_key] == 0:
            date = day[date_key]
            
            # comparing day to the latest date and adding it to list if it's the lastest
            if latest_date is None or date > latest_date:
                latest_date = date

    # if there was a day with 0 cases            
    if latest_date is not None:

        # formating date
        formatted_date = datetime.strptime(str(latest_date), '%Y%m%d').strftime('%m/%d/%Y')

        # printing output
        print("The last day with 0 new cases is:", formatted_date)

    # if no days had 0 new cases    
    else:
        print("No days with 0 new cases.")

# month with the highest new number of covid cases
def highest_month(state_dct, new_case_key, date_key):

    # creating the dictionary for the months
    monthly_cases = {}

    # looping through each entry
    for entry in state_dct:

        # converting date to string
        date_str = str(entry[date_key])

        # finding the number of cases from each entry
        new_case = entry[new_case_key]

        # formatting date and changing to months
        month_key = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m')

        # if it is a new month not in the list, it will be given a count of 0
        if month_key not in monthly_cases:
           monthly_cases[month_key] = 0

        # adding all the cases to each month
        monthly_cases[month_key] += new_case

    # finding the highest case count by month
    highest = max(monthly_cases, key=monthly_cases.get)

    # printing output
    print(highest, "was the month with the highest number of new cases at:", monthly_cases[highest])

# month with the lowest new number of covid cases
def lowest_month(state_dct, new_case_key, date_key):

    # creating the dictionary for the months
    monthly_cases = {}

    # looping through each entry
    for entry in state_dct:

        # converting date to string
        date_str = str(entry[date_key])

        # finding the number of cases from each entry
        new_case = entry[new_case_key]

        # formatting date and changing to months
        month_key = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m')

        # if it is a new month not in the list, it will be given a count of 0
        if month_key not in monthly_cases:
           monthly_cases[month_key] = 0

        # adding all the cases to each month
        monthly_cases[month_key] += new_case
    
# This was the same process as in highest_month to create the month dictionary. I tried to have a seperate function to create the monthly_cases but I got a retreval error when trying to find the max and min.

    # finding the lowest case count by month
    lowest = min(monthly_cases, key=monthly_cases.get)

    # printing output
    print(lowest, "was the month with the highest number of new cases at:", monthly_cases[lowest])  


# looping through each state to give them their own outputs
for state in states:

    ticker = state                      # ticker for putting in the url
    date_key = "date"                   # the key the json uses for the date
    new_case_key = "positiveIncrease"   # the key the json uses for the number of new cases

    # pulling data from the api that will adjust based on the state we're looping through
    url = 'https://api.covidtracking.com/v1/states/'+ ticker + '/daily.json'
    request = requests.get(url)

    # putting date into a dictionary
    state_dct = json.loads(request.text)

    
    # calling function to name state and print header
    print_state_name(state)

    # calling functions to ouput needed statistics
    average_new_cases(state_dct, new_case_key)
    highest_new_cases(state_dct, new_case_key, date_key)
    date_no_cases(state_dct, new_case_key, date_key)
    highest_month(state_dct, new_case_key, date_key)
    lowest_month(state_dct, new_case_key, date_key)
    
    # saving each states dictionary to a folder in my homework 
    folder_path = "Homework/hw5/json_files"
    saving_fil_path = folder_path + "/" + state + ".json"
    with open(saving_fil_path, 'w') as json_file:
        json.dump(state_dct, json_file)