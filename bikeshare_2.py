import time
import pandas as pd
import datetime
from pandas.io.parsers import read_csv

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Keep original columns for using to display data rows
ORIGINAL_COLUMNS = []

def check_month(month):
    """
    Checks whether month is valid month filter

    Args:
        (str) month - month name to validate
    Returns:
        (bool) - whether valid month filter or not
    """
    if month == 'all': return True
    try:
        datetime.datetime.strptime(month, '%B')
        return True
    except: 
        return False

def check_weekday(day):
    """
    Checks whether day is valid weekday filter

    Args:
        (str) day - weekday name to validate
    Returns:
        (bool) - whether valid weekday filter or not
    """
    if day == 'all': return True
    try:
        datetime.datetime.strptime(day, '%A')
        return True
    except: 
        return False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
        city = input('Please enter city name (Possible options "Chicago", "New York City" or "Washington"): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city input ..')

    # get user input for month (all, january, february, ... , june)
    while(True):
        month = input('Please enter month name or "all" for no filter: ').lower()
        if check_month(month):
            break
        else:
            print('Invalid month input ..')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        day = input('Please enter weekday name or "all" for no filter: ').lower()
        if check_weekday(day):
            break
        else:
            print('Invalid weekday input ..')

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
    df = pd.read_csv(CITY_DATA.get(city), parse_dates=["Start Time", "End Time"])
    
    # Save original columns for displaying rows later
    global ORIGINAL_COLUMNS
    ORIGINAL_COLUMNS = df.columns
    
    # Compute Month, Weekday and Hour columns to facilitate filtering and stats computation below
    df['Month'] = (df['Start Time'].dt.month_name()).str.lower()
    df['Weekday'] = (df['Start Time'].dt.day_name()).str.lower()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter by Month or Weekday if specified 
    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month: ', df['Month'].mode()[0])

    # display the most common day of week
    print('Most Common Weekday: ', df['Weekday'].mode()[0])

    # display the most common start hour
    print('Most Common Start Hour: ', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly Used Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Commonly Used End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    # Compute a new column denoting itinerary using combination of start and end station
    df['Itinerary'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most Frequent Combination Trip: ', df['Itinerary'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum(), 'seconds')

    # display mean travel time
    print('Total travel time: ', df['Trip Duration'].mean(), 'seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Type Counts: ")
    print(df['User Type'].value_counts(), '\n')

    # Display counts of gender, if gender info is present in city data
    if 'Gender' in df.columns:
        print("Gender Counts: ")
        print(df['Gender'].value_counts(), '\n')
    else:
        print('No gender info for this city')

    # Display earliest, most recent, and most common year of birth, if birth year is present in city data
    if 'Birth Year' in df.columns:
        print('Earliest Birth Year is: ', df['Birth Year'].min())
        print('Most Recent Birth Year is: ', df['Birth Year'].max())
        print('Most Common Year is: ', df['Birth Year'].mode()[0])
    else:
        print('No birthyear info for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Check if dataframe is not empty after applying filters
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # Displaying data, without the computed columns, 5 records each time
            df_to_display = df[ORIGINAL_COLUMNS]
            while(not df_to_display.empty):
                display_5_rows = input("\nWould you like to display 5 records of the data ? Enter yes or no.\n")
                if display_5_rows.lower() != 'yes':
                    break
                # Case answer is yes, print first 5 records, then drop them from dataframe and move to next iteration
                print(df_to_display.head())
                df_to_display = df_to_display.iloc[5:]

        else:
            print('Your specified filters yielded no records')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()