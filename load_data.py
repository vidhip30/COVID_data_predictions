""" The purpose of this file is to load the data and perform all the necessary dataset
transformations needed to create a pandas.DataFrame Object for the Linear Regression and
Correlation files"""

# Import modules

import csv
import pandas as pd
import datetime

# Set constants string/ dictionary to be used for the functions below

PUNCTUATION = '!\"#$%&()*+,-./:;<=>?@[]^_`{|}~'

month_to_num = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
                'June': 6, 'July': 7, 'August': 8, 'September': 9,
                'October': 10, 'November': 11, 'December': 12}


def read_death_count_data() -> list[list]:
    """Load dataset1 reading the csv reader, then transform the data into a list of datetime.date
    objects and the sum of death of counts of the three major diseases
    """

    # Create all the lists we need for the computations below

    collect_all_rows = []
    mn_lst = []  # mn stands for 'Malignant neoplasms'
    doh_lst = []  # doh stands for 'Diseases of heart'
    clrd_lst = []  # clrd stands for 'Chronic lower respiratory diseases'
    sum_lst = []  # sum the death counts of the three diseases
    num_to_remove = []

    # These are individual lists to collect the death counts of each diseases including
    # Malignant neoplasms, Diseases of heart and Chronic lower respiratory diseases

    mn_total = []
    doh_total = []
    clrd_total = []

    # Open and read the csv file

    with open('dataset.csv', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            collect_all_rows.append(row)  # Collect all the rows from the csv file into a list

        dt_lst = create_datetime(collect_all_rows)  # dt stands for datetime

        # Collect the data for just the three diseases we are grouping

        for row in collect_all_rows:

            if 'Malignant neoplasms' in row:
                mn_lst.append(row)

            elif 'Diseases of heart' in row:
                doh_lst.append(row)

            elif 'Chronic lower respiratory diseases' in row:
                clrd_lst.append(row)

                # Remove the first 2 elements in the list because they are not death counts, but rather extra data

        for _ in range(2):
            mn_lst[5].pop(0)
            doh_lst[5].pop(0)
            clrd_lst[5].pop(0)

            # Add the total number of death counts of the three diseases

        for i in range(len(mn_lst[5])):
            sum_lst.append(int(mn_lst[5][i]) + int(doh_lst[5][i]) + int(clrd_lst[5][i]))
            mn_total.append(int(mn_lst[5][i]))
            doh_total.append(int(doh_lst[5][i]))
            clrd_total.append(int(clrd_lst[5][i]))

        return_dates = remove_extra_dates(dt_lst)  # remove the extra dates that are out of timeframe

        remove = len(sum_lst) - len(return_dates)  # Calculate how many extra dates we need to remove

        mn_remove = []
        doh_remove = []
        clrd_remove = []

        for i in range(remove):
            num_to_remove.append(sum_lst[i])
            mn_remove.append(mn_total[i])
            doh_remove.append(doh_total[i])
            clrd_remove.append(clrd_total[i])

        return_nums1 = remove_extra_nums(sum_lst, num_to_remove)
        return_nums2 = remove_extra_nums(mn_total, mn_remove)
        return_nums3 = remove_extra_nums(doh_total, doh_remove)
        return_nums4 = remove_extra_nums(clrd_total, clrd_remove)

        # Return the final version of the list with the correct datetime and death counts
    # within our desired timeframe

    return [return_dates, return_nums1, return_nums2, return_nums3, return_nums4]


# Helper Functions for load_dataset1

def create_datetime(data_input: list) -> list:
    """Transform the csv file dates with English Months into datetime.date objects"""

    # Set initial lists

    collect_all_dates = []
    return_lst = []

    # Append the dates only from the input data list

    for date in data_input[0]:
        collect_all_dates.append(date)

        # Split the month, day and year into strings

    collect_all_dates = [str.split(date) for date in collect_all_dates]

    # Remove the punctuation in the date strings

    for date in collect_all_dates:
        for word in date:
            for char in word:
                if all([char in PUNCTUATION]):
                    date.remove(word)
                    blank = str.replace(word, char, '')
                    date.insert(1, blank)

                    # Transform the string dates into datetime.date objects

    for date in collect_all_dates:
        transform = datetime.date(year=int(date[2]),
                                  month=month_to_num[date[0]],
                                  day=int(date[1]))

        # Append to the return list
        return_lst.append(transform)

    return return_lst  # return the list with the dates transformed into datetime.date objects


def remove_extra_dates(dt_lst: list) -> list:
    """Remove the extra data to match the dates of both datasets"""

    # Initialize the list variables

    collect_2020_lst = []
    collect_2021_lst = []

    # Collect 2020 dates within the timeframe

    for date in dt_lst:
        if date.year >= 2020:
            collect_2020_lst.append(date)

            # Collect 2021 dates within the timeframe

    for date in collect_2020_lst:
        if date.year < 2021 and date.month >= 4:
            collect_2021_lst.append(date)
        elif date.year == 2021:
            collect_2021_lst.append(date)

            # Remove the first date to match the timeframe of dataset 1 and 2
    collect_2021_lst.remove(datetime.date(2020, 4, 4))

    return collect_2021_lst  # Return the list with the correct timeframe


def remove_extra_nums(nums: list, remove_num_lst: list) -> list:
    """Remove the extra data to match the dates of both datasets"""

    # Remove the amount of nums given to the function

    for num in remove_num_lst:
        nums.remove(num)

    return nums


def read_covid19_hospitalization_data() -> any:
    """Load Dataset2"""
    # Read csv file for second dataset
    data2 = pd.read_csv('dataset2.csv')
    data2['date'] = pd.to_datetime(data2['date'])  # convert 'date' to datetime64
    data2['date'].dt.normalize()  # time component not relevant so normalize

    """Pivot the DataFrame and include relevant information"""
    variables = ['date', 'oh_region', 'hospitalizations']  # The columns we want
    group_var = variables[:2]
    outcome_var = variables[2]
    data2 = data2.groupby(group_var, as_index=False)[outcome_var].sum()
    data2 = data2.set_index(['date', 'oh_region']).unstack('oh_region').fillna(0)  # Use dates as index
    data2.columns = data2.columns.levels[1].rename(None)

    """Checking for complete days before aggregating as weekly data"""
    # (Uncommented) check if index has all dates in the given date range
    # _days = len(data2.index.unique())  # Is 618
    date_range = pd.date_range(data2.index.min(), data2.index.max())  # len is 619, so 1 day missing
    data2_new = data2.reindex(date_range, fill_value=0)  # Fill missing day's data with 0

    # Aggregate the number of hospitalizations from regions to all on Ontario
    new_index = data2_new.index
    hosp_all_regions = (sum(data2_new[column] for column in data2_new.columns))  # concatenate
    data_hosp_on = pd.DataFrame({'Hospitalizations': hosp_all_regions}, index=new_index)

    # Use rows corresponding to the date range compatible with the death count dataset
    data_hosp_on = data_hosp_on['2020-04-05': '2021-07-31']

    data_hosp_w = data_hosp_on.resample('W-SAT').sum()  # Group by week (Sun-Sat)

    return data_hosp_w


def group_datasets() -> any:
    """Run the program and return dataframe object with the dates as index, a column for death counts
    and a column for hospitalizations"""
    # Get the values from the columns of both datasets
    dataset_columns = get_dataset_values()

    # Group the values into a dict to input into a pandas DataFrame
    grouped_dataset = {'Hospitalizations': dataset_columns[4],
                       'Sum of Death Counts': dataset_columns[0],
                       'Malignant Neoplasms d.c.': dataset_columns[1],
                       'Diseases of the Heart d.c.': dataset_columns[2],
                       'Chronic lower respiratory diseases d.c.': dataset_columns[3]}

    # Get the index (both datasets have the same dates as the index)
    dataset_index = read_death_count_data()[0]

    # Group the columns from both datasets
    final_dataset = pd.DataFrame(grouped_dataset, index=dataset_index)

    return final_dataset  # the DataFrame object that can be used by other functions


def get_dataset_values() -> tuple:
    """Return a tuple of two lists"""

    # Dataset 1 values
    counts_list = read_death_count_data()
    # Get death counts data as lists (per columns in the dataset)
    sum_list, mn_list, doh_list, cr_list = \
        counts_list[1], counts_list[2], counts_list[3], counts_list[4]

    # Dataset 2 values
    hosp_data = read_covid19_hospitalization_data()
    # Get hospitalization data as list
    hospitalizations_per_week = hosp_data['Hospitalizations'].values
    hosp_list = []
    for num in hospitalizations_per_week:
        hosp_list.append(num)

    # Values of the datasets combined
    return sum_list, mn_list, doh_list, cr_list, hosp_list
