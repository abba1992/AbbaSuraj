import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
WEEK_DATA = {   'mon': 0,
                'tues': 1,
                'wed': 2,
                'thur': 3,
                'fri': 4,
                'sat': 5,
                'sun': 6}
MONTH_DATA = { 'jan': 1,
                'feb': 2,
                'mar': 3,
                'apr': 4,
                'may': 5,
                'jun': 6}
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print("Which country's data do you want to see?")
        city = input('Type c for Chicago, n for New York City, or w for Washington. Your input is case not sensitive: ').lower()
        print()
        if city=='c':
            city='chicago'
        if city=='n':
            city='new york city'
        if city=='w':
            city='washington'
        if city not in CITY_DATA:
            print('Invalid city entry')
            continue
        city = CITY_DATA[city]
        break
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        mon_wk = input('Would you like to see data by month or week? Type Y/N: ').lower()
        print()
        if mon_wk=='y':
            mon_wk=True
        elif mon_wk=='n':
            mon_wk=False
        else:
            print('Invalid Month/Week choice entry')
            continue
        break

    while True:
        if mon_wk:
            mon_wk_filter=input("Type 'month', 'day' or 'both' to see data by month, day or both: ").lower()
            print()
            if mon_wk_filter=='month':
                print("Which month's data would you like to see? ")
                month = input('jan,feb, mar, apr, May, jun. Your entry is not case sensitive: ').lower()
                print()
                if month not in MONTH_DATA:
                    print('Invalid month entry!')
                    continue
                month = MONTH_DATA[month]
                day='all'
            elif mon_wk_filter=='day':
                print("Which days's data would you like to see? ")
                day = input('mon, tue, wed, thur, fri, sat, sun. Your entry is not case sensitive: ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Invalid month entry!')
                    continue
                day = WEEK_DATA[day]
                month='all'
            elif mon_wk_filter=='both':
                print("Which month's data would you like to see? ")
                month = input('jan, feb, mar, apr, May, jun ').lower()
                print()
                if month not in MONTH_DATA:
                    print('Invalid month entry!')
                    continue
                month = MONTH_DATA[month]
                print("Which day's data would you like to see? ")
                day = input('mon, tue, wed, thur,fri, sat, sun. Your entry is not case sensitive: ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Invalid day entry!')
                    continue
                day = WEEK_DATA[day]
            else:
                print("Invalid Entry!")
                continue
            break
        else:
            day='all'
            month='all'
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]
    df.drop('day_of_week',axis=1,inplace=True)
    df.drop('month',axis=1,inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    # TO DO: display the most common month
    most_freq_mm = df['month'].mode()[0]
    for mm in MONTH_DATA:
        if MONTH_DATA[mm]==most_freq_mm:
            most_freq_mm = mm.title()
    print(f'{most_freq_mm} is the most common month for travel')
    # TO DO: display the most common day of week
    most_freq_dd = df['day_of_week'].mode()[0]
    for ww in WEEK_DATA:
        if WEEK_DATA[ww]==most_freq_dd:
            most_freq_dd = ww.title()
    print(f"{most_freq_dd} is the most common day for travel")

    # TO DO: display the most common start hour
    df['hour']=pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hh = df['hour'].mode()[0]
    print(f"{most_freq_hh} is the most common hour for travel")
    df.drop('hour',axis=1,inplace=True)
    df.drop('day_of_week',axis=1,inplace=True)
    df.drop('month',axis=1,inplace=True)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print()
    print(f"Most commonly used start station is: {df['Start Station'].mode()[0]}")

    # TO DO: display most commonly used end station
    print()
    print(f"Most commonly used end station is: {df['End Station'].mode()[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    print()
    most_freq_sttn_combo = df['Start Station'] + df['End Station']
    print(f"The most frequent combination of start station and end station trip is: {most_freq_sttn_combo.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # TO DO: display total travel time
    print()
    tt_travel = df['Trip Duration'].sum()
    print(f"Total travel time was: {tt_travel}")
    
    # TO DO: display mean travel time
    print()
    mean_tt = math.ceil(df['Trip Duration'].mean())
    
    print(f" The Mean travel time was: {mean_tt}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print()
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    print()

    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")
    

    # TO DO: Display earliest, most recent, and most common year of birth
    print()
    
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_cmon = df['Birth Year'].value_counts()
        print(f'The earliest year of birth is: {earliest}')
        print(f'The earliest year of birth is: {earliest}')
        print(f'The most common year of birth is: {most_cmon}')
    except:
        print("Birth year details do not exist here.")
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #Script should prompt the user if they want to see 5 lines of raw data, display that data if the answer is 'yes', and continue these #prompts and displays until the user says 'no'.

def User_Response(df):
    #Code (while)for user based on whether they want to view raw data or not
    #And how much they will want to view from the data when it appears
    response_one = ['y', 'n']
    response_two = ['y', 'n']
    response_a = ''
    response_b = ''

    more_data = 0
    while response_a not in response_one:
        response_a = input("There are raw data available. Would you like to see them? Type Y/N: ").lower()
        if response_a == "y":
            response_b = input("Would you like to view data from top (t) or bottom (b)? Type T/B").lower()
            if response_b == 't':
                print(df.head())
            elif response_b == 'b':
                print(df.tail())
        elif response_a not in response_one:
            print("Invalid user response")

    #would the user want to view more of data?
    while response_a == 'y':
        response_more = input("Want to view more? Type Y/N: ").lower()
        more_data += 5
        if response_more == "y":
             print(df[more_data:more_data+5])
        elif response_more == "n":
             break

    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        User_Response(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()