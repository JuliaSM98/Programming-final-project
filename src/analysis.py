"""! @brief Analysis of data (Part III) \n
    This module generates the files or visualization tools to analyse previously obtained results.
"""


##
# @file analysis.py
#
# @brief Python program corresponding to the third part of the final project.
#
# @section description_analysis Description
# This part of the programme corresponds to the analysis of the results obtained in the previous section.
# Here, visualisation tools are used to graphically display the results obtained in order to facilitate their
# analysis. The values obtained for the return and volatility of the different portfolios (investment strategies)
# are analysed using different graphs.
#
# @section libraries_analysis Libraries/Modules
# - pandas library (https://pypi.org/project/pandas/)
#   - Access to Dataframes, Series, etc.
# - matplotlib library (https://pypi.org/project/matplotlib/)
#   - Access to ploting functionalities
# - seaborn library (https://pypi.org/project/seaborn/)
#   - Access to ploting functionalities (friendly with pandas)
#
# @section author_analysis Author(s)
# - Created by group number 5 on March of 2022.
#


# Imports
import pandas as pd
import matplotlib.pyplot as plt
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
    distributionReturns(dfs.get("METS"))

def showQuadrant(df:pd.DataFrame) -> None:
    """! Plots a scatterplot with the using the return & volatility values contained on DataFrame, to show the relation between both variables. 
        @param df The dataframe to be used
    """
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
    plt.title(f"Volatility vs Return")

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

def distributionReturns(df:pd.DataFrame) -> None:
    """! Plots a barchart with the distribution of the returns for the generated data between 01/2020 and 31/12/2020, using the DataFrame provided. 
        @param df The dataframe to be used
    """
    # -- Distribution of the returns for the generated data between 01/2020 and 31/12/2020 --
    # -- Print Plot --
    plt.figure(figsize=(12, 8))

    #Hisogram + distribution plot
    sns.histplot(df, x="RETURN", kde=True)

    #Title
    plt.title(f"Return distribution")

    # x and y axis labels
    plt.xlabel("Return")
    plt.ylabel("Count + Density")

    plt.show()


if __name__ == "__main__":
    main()