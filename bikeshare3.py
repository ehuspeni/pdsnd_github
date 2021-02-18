import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():

    city = input('What city would you like to analyze? (chicago, new york city, or washington):').lower()
    while city not in CITY_DATA.keys():
        print("Oops! That isn't a valid city input. Please specify chicago, new york city, or washington")
        city = input('What city would you like to analyze? (chicago, new york city, or washington):').lower()
    else:
        print('Great! Let\'s look at {}'.format(city))

    month = input('What month would you like to look at? (please specify a month or type "all"):').lower()
    while month not in months:
        print("Oops! That isn't a valid month input. Please specify a month between january and june or type 'all'")
        month = input('What month would you like to look at? (please specify a month or type "all"):').lower()
    else:
        print('Great! Let\'s look at {}'.format(month))

    day = input('What day of the week would you like to look at? (please specify day or type "all"):').lower()
    while day not in days:
        print("Oops! That isn't a valid day input. Please specify a day of the week or type 'all'")
        day = input('What day of the week would you like to look at? (please specify day or type "all"):').lower()
    else:
        print('Great! Let\'s look at {}'.format(day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    #Loads data for the specified city and filters by month and day if applicable.
    filename = 'C:/Users/Elaine/OneDrive/Documents/Udacity/Python/udacity-git-course/pdsnd_github/.ignorefiles/' + str(CITY_DATA[city])

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]

    # display the most common day of week
    pop_day = df['day'].mode()[0]


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]

    print('Most common month is {}.\nMost common day is {}. \nMost common start hour is {}.'.format(pop_month, pop_day, pop_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    pop_trip = df['trip'].mode()[0]

    print('Most common start station is {}. \nMost common ending station is {}. \nMost common trip is {}.'.format(pop_start_station, pop_end_station, pop_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End'] = pd.to_datetime(df['End Time'])
    df['travel_time'] = (df['End'] - df['Start Time'])
    total_trav_time = df['travel_time'].sum()

    # display mean travel time
    mean_travel_time = df['travel_time'].mean()

    print('Total number of hours of travel time is {}. \nAverage trip duration is {}.'.format(total_trav_time, mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
    else:
        gender = "NA"
        print('Unfortunately, this dataset does not contain gender information.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
    else:
        oldest = 'NA'
        youngest = 'NA'
        common_year = 'NA'
        print('Birth year information is not included in this dataset, sorry.')

    print('User type breakdown is:\n{} \n\nGender of users is:\n{}\n\n Earliest birth year is: {}\n Most Recent birth year is: {}\n Most common birth year is: {}'.format(users, gender, oldest, youngest, common_year))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
