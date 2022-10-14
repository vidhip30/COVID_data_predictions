""""Description"""

import matplotlib.pyplot as plt
from load_data import group_datasets


def retrieve_data() -> tuple:
    """retrieve data"""
    data = group_datasets()

    # collecting hospitalization data and total death counts
    hosp = data['Hospitalizations'].values
    sum_death_counts = data['Sum of Death Counts'].values

    return hosp, sum_death_counts


def generate_best_fit_line() -> tuple:
    """Calculate the line of best fit"""
    hosp, death_counts = retrieve_data()

    # calculating mean of hospitalization and total death counts
    mean_hosp = sum(hosp) / len(hosp)
    mean_death_count = sum(death_counts) / len(death_counts)

    total_values = len(hosp)

    # calculating slope and y-int of the line
    num = 0
    den = 0

    for i in range(0, total_values):
        num = num + ((hosp[i] - mean_hosp) * (death_counts[i] - mean_death_count))
        den = den + (hosp[i] - mean_hosp) ** 2

    slope = num / den
    y_int = mean_death_count - (slope * mean_hosp)
    coeff = (slope, y_int)

    return coeff


def get_regression_line() -> None:
    """function that plots the scatter plot and regression line of the given data using the inputs
    hosp, death_counts and coeff which is a tuple consisting of the slope and y-int of the line.
    """
    hosp, death_counts = retrieve_data()
    coeff = generate_best_fit_line()
    # creating a scatter plot for the given points
    plt.scatter(hosp, death_counts, color="g", marker="s", s=50)

    # predicted death counts
    y_predicted = (coeff[0] * hosp) + coeff[1]

    # plot the linear regression line
    plt.plot(hosp, y_predicted, color="b")

    # labelling the x and y axis
    plt.xlabel('Hospitalizations')
    plt.ylabel('Total Death Counts')

    plt.show()


get_regression_line()
