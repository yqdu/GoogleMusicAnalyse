# Weighted Ranking by true Bayesian estimate (WR) = (v / (v+m)) * R + (m / (v+m)) * A
# R = rating, regular average for the song (mean)
# v = votes number
# m = minimum vote number for entering ranking list
# A = Average ranking in the database

import pandas as pd
import scipy as sp
from matplotlib import pyplot as plt

# Reading data locally
df = pd.read_csv('raw.csv')

# different songs under same album shares all information beyond urls, so weed to wash it
# wash songs data into albums data
df = df.drop_duplicates()

# save albums data
df.to_csv('washed.csv')

# the unweighted rank
df.sort_values(by='Rating', ascending=False).to_csv('unweighted-ranked.csv')

A = sp.mean((df.ix[:, 1]))

v = df.ix[:, 3]

m = 500

R = df.ix[:, 1]

WR = (v / (v + m)) * R + (m / (v + m)) * A

right = pd.DataFrame({'WR': WR})

ranked = df.join(right)

# sorted rank
sr = ranked.sort_values(by='WR', ascending=False)

# save ranks
sr.to_csv('weighted-ranked.csv')

#get top 500
top = sr[0:500]

# the top list
top.to_csv('top.csv')

# year distribution. we can see which year produces the most number of popular songs
year = top.ix[:, 6].value_counts()
# category distribution. we can see which kind of music is the most popular
category = top.ix[:, 0].value_counts()
# company distribution. we can see which company produces the most number of popular songs
company = top.ix[:, 5].value_counts()

pd.options.display.mpl_style = 'default'

plt.show(year.plot(kind = 'bar'))

plt.show(category.plot(kind = 'bar'))

plt.show(company.plot(kind = 'bar'))

# ratio between the top 500 number of a kind of music and its total number
# we can see which kind of music is easier to be popular
plt.show(((top.ix[:, 0].value_counts())/(sr.ix[:, 0].value_counts())).plot(kind = 'bar'))

#
#
# #get worst 1000
# low = sr[len(sr)-1001:len(sr)-1]
#
# year = low.ix[:, 6].value_counts()
#
# category = low.ix[:, 0].value_counts()
#
# camp = low.ix[:, 5].value_counts()
#
# plt.show(year.plot(kind = 'bar'))
#
# plt.show(category.plot(kind = 'bar'))
#
# plt.show(camp.plot(kind = 'bar'))