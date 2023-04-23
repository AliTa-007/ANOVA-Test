import numpy as np
import statistics
import pandas as pd

# Need help with your repetitive and tedious ANOVA calculations?
# master will be our dataset which will include lists of the different samples AKA siblings

master = []
sibling = []
input("Welcome to my ANOVA Assistant")
k = int(input("Sample Count?"))

for c in range(k):
    sibling = []
    n = int(input("Sample Size?"))
    for x in range(n):
        sibling.append(float(input("Value?")))
    master.append(sibling)

grand_mean = np.average(list(np.concatenate(master).flat))
ss_b = 0
ss_w = 0
for sibling in master:
    ss_b = ss_b + len(sibling) * (np.average(sibling) - grand_mean) ** 2
    ss_w = ss_w + (len(sibling) - 1) * statistics.variance(sibling)
sstotal = ss_b + ss_w

df_b = len(master) - 1
df_t = len(list(np.concatenate(master).flat)) - 1
df_w = df_t - df_b

ms_b = ss_b / df_b
ms_w = ss_w / df_w

f_test = ms_b / ms_w

table = [[ss_b, df_b, ms_b, f_test], [ss_w, df_w, ms_w, f_test]]
df = pd.DataFrame(table, columns = ['SS', 'DF', 'MS', 'F'], index=['Between', 'Within'])
print(df)