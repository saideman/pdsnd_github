import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = [ 'january','february','march','april','may','june','all' ]
DAYS_OF_WEEK = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

def sec_convert(seconds): 
    days = seconds // (86400)
    seconds = seconds % (86400)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    converted = [int(days),int(hours),int(minutes),seconds]
      
    return converted


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid         inputs
    city = input('Which city would you like to explore, Chicago, New York City or Washington? ').lower()
    while city not in CITY_DATA:
        city = input('That is not a valid city, please enter Chicago, New York City or Washington. ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('What month shall we analyze? Please enter All or a month, January through June. ').lower()
    while month not in MONTHS:
        month = input('That is not a valid month, please enter All or a month, January through June. ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week? Please enter All or a specific day. ').lower()
    while day not in DAYS_OF_WEEK:
        day = input('That is not a valid day, please enter All or a specific day like Monday. ').lower()

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
    #Load Data
    df = pd.read_csv(CITY_DATA[city])
    
    #Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #Create month and day columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #Filter by month
    if month != 'all':
        monthindex = MONTHS.index(month) + 1
        df = df[df['month'] == monthindex]
    
    #Filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df                                                      
                           
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    freq_month = MONTHS[df['month'].mode()[0] - 1].capitalize()
    print('The most frequent month of travel is', freq_month)

    # TO DO: display the most common day of week
    freq_day = df['day_of_week'].mode()[0]
    print('The most frequent day of travel is', freq_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    freq_hour = str(df['hour'].mode()[0]) +':00'
    print('The most frequent hour of travel is', freq_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    freq_start = df['Start Station'].mode()[0]
    print('The most frequently used journey start station is', freq_start)

    # TO DO: display most commonly used end station
    freq_end = df['End Station'].mode()[0]
    print('The most frequently used journey end station is', freq_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    freq_trip = df['trip'].mode()[0]
    print('The most frquent trip is from', freq_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    rent_time = sec_convert(df['Trip Duration'].sum())
    print('Total usage time for all bikes was {} days, {} hours, {} minutes and {} seconds'.format(*rent_time))
          
    # TO DO: display mean travel time
    avg_rent_time = sec_convert(df['Trip Duration'].mean())
    print('The average time of each ride was {2} minutes and {3} seconds'.format(*avg_rent_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('The following is a count of user types that rode:')
    print(user_count.to_string())
    
    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('\nAnd the following is a count by gender (if known):')
        print(gender_count.to_string())
    else:
        print('\nThere is no gender data available for this city')
   
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        freq_year = df['Birth Year'].mode()[0]
        
        print('\nAlthough not all riders provided their birth dates, amongst those that did:')
        print('The oldest rider was born in', int(earliest_year))              
        print('The youngest rider was born in', int(latest_year))
        print('The most common year of birth was',int(freq_year))
    else:
        print('\nThere is no age data available for this city')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def show_raw_data(df):
    """Displays raw data in blocks of 5 rows while user input is yes."""

    show_data = input('\nWould you like to see the first five rows of raw data? Enter yes or no. ').lower()
    if show_data == 'yes':
        df = df.drop(columns=df.columns[[0]])
        df = df.drop(columns=['month', 'day_of_week', 'hour', 'trip'])
        i = 0
        while True:
            print()
            for ii in range(i,i+5,1):
                data = df.iloc[i]
                print(data)
                print('-'*60)
                i += 1                
            next_data = input('\nWould you like to see the next five rows? Enter yes or no. ').lower
            if next_data() != 'yes':
                break
               
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()    