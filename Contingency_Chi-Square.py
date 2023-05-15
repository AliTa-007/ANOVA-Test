import numpy as np
import pandas as pd
import scipy.stats


# I think you can take the columns as an input and specify the pd.Dataframe with no problems


class Table:
    def __init__(self, r, c, column_list, index_list):
        self.content_sum = None
        self.row_sum = None
        self.row_count = r
        self.col_count = c
        self.dof = (self.row_count - 1) * (self.col_count - 1)
        self.content = pd.DataFrame(np.zeros((r, c)), columns=column_list, index=index_list)
        self.total = None
        # self.row_sum = pd.concat([self.content, pd.Series(self.content.sum(axis=1), name='R_Sum')], axis=1)
        # self.col_sum = pd.concat([self.content, pd.Series(self.content.sum(axis=0), name='C_Sum')], axis=0)
        # self.content_sum = pd.concat([self.row_sum, pd.Series(self.content.sum(axis=0), name='C_Sum')], axis=0)

    def get_shape(self):
        return self.row_count, self.col_count

    def set_row(self, r, array):
        self.content.iloc[r] = array

    def __str__(self):
        return "{}".format(self.content)

    # Append is going to be removed. For pd.concat to work you must add two dataframe objects with the same EXACT layout
    def sum_table(self):
        self.total = self.content.sum().sum()
        self.row_sum = pd.concat([self.content, pd.Series(self.content.sum(axis=1), name='R_Sum')], axis=1)
        self.content_sum = self.row_sum.append(pd.Series(self.row_sum.sum(axis=0), name='C_Sum'), ignore_index=True)
        return "{}".format(self.content_sum)


print("Welcome. This is Ali Tasbas' Chi-Square test for contingency tables. \n First things first. Some formats to "
      "help you input the correct table.\n 1. Populations are horizontal placed as rows\n 2.Attributes are vertical "
      "placed as columns\n 3.After pop and attributes all inputs are required to be in a list format. eg.[a,b,c]\n More to come...")
r = int(input("Population count: "))
c = int(input("Attribute count: "))
ind_list = eval(input("Population names: "))
col_list = eval(input("Attribute names: "))
data = Table(r, c, col_list, ind_list)


for i in range(r):
    lis = eval(input("Population values: "))
    data.set_row(i, lis)

data.sum_table()
df = data.content_sum
# cell_coordinates = eval(input("Which two cells are you planning on conducting a test? (Enter as a list of coordinates "
#                               "eg. [[row1,column1],[row2, column2]]) \n"))
print(df)
# num = 0
# We can put p_bar inside the for, but this is more readable for a statistician.
# for cell in cell_coordinates:
#     num += data.content.iloc[cell]
# p_bar = num / data.total

expected_data = data.content.copy()
for r in range(data.row_count):
    for c in range(data.col_count):
        expected_data.iloc[r, c] = df.iloc[r, -1] * df.iloc[-1, c]
expected_data = expected_data / data.total

# TODO Add this functionality to the class itself. Make the process automatic.

# TODO Conduct the Chi-Square result. For every cell, (f_obs - f_e)^2 / f_e
chi_test = (((data.content - expected_data) ** 2) / expected_data).sum().sum()
chi_crit = scipy.stats.chi2.ppf(1-0.05, df=1)

if chi_test > chi_crit:
    print("There seems to be concrete evidence to suggest unequal proportions")
elif chi_test < chi_crit:
    print("We can't imply a difference exists between the populations")
else:
    print("How in the world did you get this? I'm speechless")
