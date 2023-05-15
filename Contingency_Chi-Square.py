import numpy as np
import pandas as pd
import scipy.stats
from tabulate import tabulate


# I think you can take the columns as an input and specify the pd.Dataframe with no problems


class Table:
    def __init__(self):
        self.row_count = 0
        self.col_count = 0
        self.dof = 1
        self.content = None
        self.alpha = 0.05
        self.row_sum = None
        self.col_sum = None
        self.content_sum = None
        self.total_size = None
        self.expected_content = None

    # Possibly Initialize the table with this "method"
    def create_table(self):
        n_row = int(input("Population count: "))
        n_col = int(input("Attribute count: "))
        index_list = eval(input("Population names: "))
        column_list = eval(input("Attribute names: "))

        self.row_count = n_row
        self.col_count = n_col
        self.dof = (self.row_count - 1) * (self.col_count - 1)
        self.content = pd.DataFrame(np.zeros((n_row, n_col)), columns=column_list, index=index_list)

        for row in range(n_row):
            array = eval(input("Population values: "))
            self.content.iloc[row] = array

        self.total_size = self.content.sum().sum()
        self.sum_table()
        self.expect_table()

    def get_created_table(self):
        return self.content

    # Append is going to be removed. For pd.concat to work you must add two dataframe objects with the same EXACT layout
    def sum_table(self):
        self.row_sum = pd.concat([self.content, pd.Series(self.content.sum(axis=1), name='R_Sum')], axis=1)
        self.col_sum = self.content.append(pd.Series(self.content.sum(axis=0), name='C_Sum'), ignore_index=True)
        self.content_sum = self.row_sum.append(pd.Series(self.row_sum.sum(axis=0), name='C_Sum'), ignore_index=True)

    def get_summed_table(self):
        return self.content_sum

    def expect_table(self):
        self.expected_content = self.content.copy()
        for row in range(self.row_count):
            for col in range(self.col_count):
                self.expected_content.iloc[row, col] = self.content_sum.iloc[row, -1] * self.content_sum.iloc[-1, col]
        self.expected_content = self.expected_content / self.total_size

    def get_expected_table(self):
        return self.expected_content

    def test(self, a=0.05):
        chi_test = round((((self.content - self.expected_content) ** 2) / self.expected_content).sum().sum(), 3)
        chi_crit = round(scipy.stats.chi2.ppf(1 - a, df=self.dof), 3)

        print(tabulate(self.get_created_table(), headers='keys', tablefmt='psql'))
        print(tabulate(self.get_expected_table(), headers='keys', tablefmt='psql'))
        # print(tabulate(self.get_expected_table(), headers='keys', tablefmt='psql'))

        print("Test statistic: " + str(chi_test) + "\nCritical Value: " + str(chi_crit))

        if chi_test > chi_crit:
            print("There seems to be concrete evidence to suggest unequal proportions")
        elif chi_test < chi_crit:
            print("We can't imply a difference exists between the populations")
        else:
            print("How in the world did you get this? I'm speechless")

    def get_shape(self):
        return self.row_count, self.col_count

    def __str__(self):
        return "{}".format(self.content)


print("Welcome. This is Ali Tasbas' Chi-Square test for contingency tables. \n First things first. Some formats to "
      "help you input the correct table.\n 1. Populations are horizontal placed as rows\n 2.Attributes are vertical "
      "placed as columns\n 3.After pop and attributes all inputs are required to be in a list format. eg.[a,b,c]\n More to come...")

data = Table()
data.create_table()
data.test(0.05)
