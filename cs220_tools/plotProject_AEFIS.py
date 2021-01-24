import os
import pandas as pd
from pandas import DataFrame, Series
import matplotlib
from matplotlib import pyplot as plt

matplotlib.rcParams["font.size"] = 12

s = Series(
    {
        "Not at all useful": 0,
        "Of very little use": 3,
        "Of little use": 2,
        "Moderately useful": 19,
        "Useful": 43,
        "Very useful": 113,
        "Extremely useful": 190 
    }
)

ax = s.plot.barh()
ax.grid(axis = "x", ls = "--")
ax.set_xlabel("Students ratings")
fig = ax.get_figure()
#ax.set_xticks(range(7))
print(list(s.index))
#ax.set_xticklabels(ax.get_xticklabels(), rotation = 45)
fig.savefig("project_scores.png", bbox_inches='tight')
