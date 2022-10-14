"""This is a sample Python script."""
import linear_reg
import correlation
import pprint

if __name__ == '__main__':
    print('We have attempted to find a relationship between the number of weekly hospitalizations '
          'due to COVID-19 and the number of weekly deaths from other kinds of diseases. \n')
    print('Enter \"1\" to see the correlation or \"2\" to see the regression line.')
    number = input()

    if number == '1':
        print(correlation.pearson())
    elif number == '2':
        linear_reg.get_regression_line()
    else:
        print('Invalid number.')
