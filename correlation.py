""" CSC110 Fall 2021 Final Project: Pearson Correlation

Module Description
==================
This Python file calculates the Pearson coefficient of the data.

Copyright and Usage Information
===============================
This file is provided solely for the use of grading the final project of CSC110 by
the TA's and instructors of the department of Computer Science at the University of Toronto St. George campus.
Modification, usage and distribution of this code for any other purpose is prohibited.

This file is Copyright (c) 2021 Anna Lee Pantoja, Savanna Pan, Tanvi Patel, Vidhi Patel.



"""

from load_data import group_datasets
import numpy as np
import math

DATA = group_datasets()


# deaths = DATA['Sum of Death Counts'].values
# hospital = DATA['Hospitalizations'].values


def pearson(deaths: list, hospital: list) -> int:
    """Calculates the Pearson Coefficient"""
    n = len(deaths)
    # loop accumulators for calculating the sum of xy^2, x^2 and y^2
    xy_so_far = 0
    x_squared_so_far = 0
    y_squared_so_far = 0
    for i in (range(n)):
        xy_so_far += deaths[i] * hospital[i]
        x_squared_so_far += deaths[i] ** 2
        y_squared_so_far += hospital[i] ** 2
    # calculates the numerator of the formula
    num = (n * xy_so_far) - ((sum(deaths)) * (sum(hospital)))
    # calculates part of the denominator of the formula
    den1 = n * x_squared_so_far - (sum(deaths)) ** 2
    # calculates second part of the denominator of the formula
    den2 = n * y_squared_so_far - (sum(hospital)) ** 2
    # calculates the final value of the denominator of the formula
    den = math.sqrt(den1) * math.sqrt(den2)
    return num / den


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'allowed-io': [],
        'extra-imports': ['python_ta.contracts', 'load_data', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
    }, output='pyta_report.html')
