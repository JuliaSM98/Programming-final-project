"""! @brief Analysis of data (Part III) \n
    This module generates the files or visualization tools to analyse previously obtained results.
"""


##
# @file analysis.py
#
# @brief Python program corresponding to the third part of the final project.
#
# @section description_strategy Description
# This programme carries out the whole process of generating and analysing investment strategies, in
# relation to the second part of the final project of the 'Programming for Data Science' course. First
# of all, the process of generating strategies with their corresponding indicators (return, volatility)
# is carried out, and then the results are analysed by means of visualisation methods and the like.
#
# @section libraries_main Libraries/Modules
# - pandas library (https://pypi.org/project/pandas/)
#   - Access to Dataframes, Series, etc.
# - itertools library (built-in package)
#   - Access to iterators (for example, iterrows)
# - math library (built-in package)
#   - Access to operations (for example, pow)
# - numpy library (https://pypi.org/project/numpy/)
#   - Access some variables (for example, nan)
#
# @section author_strategy Author(s)
# - Created by group number 5 on March of 2022.
#


# Imports
import pandas as pd
from itertools import product
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.__config__ import show
import seaborn as sns


# Global Constants
## Path to portfolio metrics data source.
PORT_METRICS = "../output/portfolio_metrics.csv"


# Functions
def init() -> dict:
    """! Initializes the program. Reads data from data sources into DataFrames & create allocations DataFrame. 
        @return Dictionary with DataFrames generated from data sources
    """

    # Return DataFrames
    return {
        "METS": pd.read_csv(PORT_METRICS),
    }

def main() -> None:
    """! Main program entry."""
    dfs = init()
    showQuadrant(dfs.get("METS"))

def showQuadrant(df:pd.DataFrame) -> None:
    # -- Standarize & Normalize: Return and Volatility --
    tmpdf = df.copy()
    tmpdf['RETURN'] = tmpdf['RETURN'].div(100)
    tmpdf['VOLAT'] = tmpdf['VOLAT'].div(100)
    tmpdf['RETURN'] = (tmpdf['RETURN'] - tmpdf['RETURN'].min()) / (tmpdf['RETURN'].max() - tmpdf['RETURN'].min())
    tmpdf['VOLAT'] = (tmpdf['VOLAT'] - tmpdf['VOLAT'].min()) / (tmpdf['VOLAT'].max() - tmpdf['VOLAT'].min())

    print(tmpdf)

    # -- Print Plot --
    plt.figure(figsize=(12,8))

    #Scatterplot
    sns.scatterplot(data=tmpdf, x='RETURN', y='VOLAT')

    #Title 
    plt.title(f"G 20 Countries : Volatility vs Return")

    # x and y axis labels
    plt.xlabel("Volatility")
    plt.ylabel("Return")

    # Set axes limit

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    #Country names
    for i in range(tmpdf.shape[0]):
            plt.text(tmpdf["VOLAT"][i], y=tmpdf["RETURN"][i], s=tmpdf.index[i], alpha=0.8)

    #Quadrant Marker          
    plt.text(x=0.9, y=0.1, s="Q4",alpha=0.7,fontsize=14, color='b')
    plt.text(x=0.1, y=0.1, s="Q3",alpha=0.7,fontsize=14, color='b')
    plt.text(x=0.1, y=0.9, s="Q2", alpha=0.7,fontsize=14, color='b')
    plt.text(x=0.9, y=0.9, s="Q1", alpha=0.7,fontsize=14, color='b')          

    # Benchmark Mean values          
    plt.axhline(y=tmpdf["RETURN"].mean(), color='k', linestyle='--', linewidth=1)           
    plt.axvline(x=tmpdf["VOLAT"].mean(), color='k',linestyle='--', linewidth=1) 
            
    plt.show()




if __name__ == "__main__":
    main()