import time
import datetime
import pandas as pd
import numpy as np

#Bring the washington-csv in the correct form
df3 = pd.read_csv("washington.csv")
df3['Trip Duration'] = df3['Trip Duration'].astype(int)
df3['Gender'] = 'Unknown'
df3['Birth Year'] = np.nan
df3.to_csv(r'washington2.csv')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington2.csv',
              'all_cities': 'all_cities.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # listing all possible inputs of cities, months and days

    cities = ['all_cities', 'chicago', 'new york city', 'washington']
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # asking for input until the correct form is given
    while True:
        city = str(input("Please enter a city name from chicago, new york city and washington or all_cities: ").lower())
        if city in cities:
            print('Your input was \"{}\"'.format(city).title())
            while True:
                month = str(input("Please enter a month name from January to June or \"all\" for the whole year: ").title())
                if month in months:
                    print('Your input was \"{}\"'.format(month))
                    while True:
                        day = str(input("Please enter a day name or \"all\" for the whole week: ").title())
                        if day in days:
                            print('Your input was \"{}\"'.format(day))
                            print('-'*40)
                            return city, month, day
                        else:
                            print('Your input was \"{}\" and not an input from {}. Try again!'.format(day, days))
                else:
                    print('Your input was \"{}\" and not an input from {}. Try again!'.format(month, months))
        else:
            print('Your input was \"{}\" and therefore not chicago, new york city or washington. Try again!'.format(city))

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

    # import data and fill nan values
    df = pd.read_csv(CITY_DATA[city])
    df['Gender'] = df['Gender'].fillna('Unknown')
    df['Birth Year'] = df['Birth Year'].fillna(np.nan)

    # Create months and weekdays as new columns to filter
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_name'] = df['Start Time'].dt.month.apply(lambda x: {1: 'January',  2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}[x])
    df['weekday'] = df['Start Time'].dt.weekday_name

    # set filtersfor months, days or "all"
    if month != 'All':
        cond1 = (df['month_name'] == month)
        df = df[cond1]

    if day != 'All':
        cond2 = (df['weekday'] == day)
        df = df[cond2]

    count_row = df.shape[0]
    print('In your selected timeframe {} rentals occurred.\n'.format(count_row))
    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['Start Time'].dt.month.apply(lambda x: {1: 'January',  2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}[x])
    popular_month = df['month'].mode()[0]
    print('The most common month is {}.'.format(popular_month))

    # TO DO: display the most common day of week
    df['weekday'] = df['Start Time'].dt.weekday_name
    popular_weekday = df['weekday'].mode()[0]
    print('The most popular day of the week is {}.'.format(popular_weekday))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is {}:00.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most frequent start station is {}.'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most frequent end station is {}.'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Merge'] = df['Start Station'].str.cat(df['End Station'],sep=" and ends at ")
    popular_start_end_combination = df['Start_End_Merge'].value_counts().idxmax()
    print('The most frequent rental starts at {}.'.format(popular_start_end_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum() / 60
    total_time = "{:.0f}".format(total_time)
    print('The total rental duration is {} minutes.'.format(total_time))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean() / 60
    mean_time = "{:.2f}".format(mean_time)
    print('The mean rental duration is {} minutes.'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('The user segments are:\n {}.'.format(user_count))

    # TO DO: Display counts of gender
    gender_distribution = df['Gender'].value_counts()
    print('\nThe gender counts are:\n {}'.format(gender_distribution))

    # TO DO: Display earliest, most recent, and most common year of birth
    if (df['Birth Year'].isnull().sum()) != df.shape[0]:
        oldest_age = df['Birth Year'].min().astype(int)
        youngest_age = df['Birth Year'].max().astype(int)
        mean_age = df['Birth Year'].median().astype(int)
        print('\nThe earliest year of birth is {}, the most recent is {} and the most common is {}.'.format(oldest_age, youngest_age, mean_age))
    else:
        print('\nYour selection doesn\'t contain brith years!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print('Your selection leads to an empty DataFrame. Please try again with different inputs!')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        display_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        while display_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_display = input('Do you wish to continue?: ').lower()
            if view_display.lower() != 'yes':
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
                break

if __name__ == "__main__":
	main()
