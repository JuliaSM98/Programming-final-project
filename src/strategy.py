"""! @brief Strategy generation (Part II) \n
    This module generates the files related to the comparison and analysis of investment strategies.
"""


##
# @mainpage Programming Final Project
#
# @section description_main Description
# Python program corresponding to the second part of the final project corresponding to the subject
# 'Programming for Data Science'. It is related to back-testing and analysis of investment strategies.
#
# @section notes_main Notes
# - The program has been executed under Python version 3.8.8.
# - The directory structure and additional information is detailed in the README file of the repository.
#


##
# @file strategy.py
#
# @brief Python program corresponding to the second part of the final project.
#
# @section description_strategy Description
# This programme carries out the whole process of generating and analysing investment strategies, in
# relation to the second part of the final project of the 'Programming for Data Science' course. First
# of all, the process of generating strategies with their corresponding indicators (return, volatility)
# is carried out, and then the results are analysed by means of visualisation methods and the like.
#
# @section libraries_strategy Libraries/Modules
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


# Global Constants
## Path to global stock data source.
ORG_GLOBAL_STOCK = "../data/amundi-msci-wrld-ae-c.csv"
## Path to corporate bonds data source.
ORG_CORP_BONDS = "../data/ishares-global-corporate-bond-$.csv"
## Path to gold data source.
ORG_GOLD = "../data/spdr-gold-trust.csv"
## Path to cash data source.
ORG_CASH = "../data/usdollar.csv"
## Path to government bonds data source.
ORG_GOVERN_BONDS = "../data/db-x-trackers-ii-global-sovereign-5.csv"
## Non-useful columns from data sources.
NON_USE_COLS_DS = ['Open','High','Low']
## The asset list to be used.
ASSETS = ['ST','CB','PB','GO','CA']
## The starting date of the analysis.
START_DATE = "2020-01-01"
## The ending date of the analysis.
END_DATE = "2020-12-31"


# Functions
def init() -> dict:
    """! Initializes the program. Reads data from data sources into DataFrames & create allocations DataFrame. 
        @return Dictionary with DataFrames generated from data sources
    """
    # Set Pandas options
    pd.options.mode.chained_assignment = None
    # Return DataFrames
    return {
        "DFST": pd.read_csv(ORG_GLOBAL_STOCK),
        "DFCB": pd.read_csv(ORG_CORP_BONDS),
        "DFGO": pd.read_csv(ORG_GOLD),
        "DFCA": pd.read_csv(ORG_CASH),
        "DFPB": pd.read_csv(ORG_GOVERN_BONDS),
        "ALLOC": pd.DataFrame(columns=ASSETS)
    }

def main() -> None:
    """! Main program entry."""

    print(f"{'[0]':<10}{' Setting up the environment ':*^70}")
    print(f"{'[0.1]':<10}{' Load data from data sources ':*^70}")
    dfs = init()
    for key, item in dfs.items(): showDf(key, item, 5, 10, False)
    print(f"\n{'[0.2]':<10}{' Clean data frames ':*^70}")
    for key, item in dfs.items(): 
        if key != "ALLOC": cleanDf(item)
        showDf(key, item, 5, 10, True)
    print(f"\n{'[0.3]':<10}{' Add missing dates & Interpolate ':*^70}")
    for key, item in dfs.items(): 
        if key != "ALLOC": dfs[key] = interpolateMissings(item)
        showDf(key, dfs[key], 5, 10, True)
    print(f"\n{'[1]':<10}{' Investment strategy generation ':*^70}")
    print(f"{'[1.1]':<10}{' Portofolio allocation ':*^70}")
    allocPortDf(dfs.get("ALLOC"))
    showDf("ALLOC", dfs.get("ALLOC"), 5, 10, False)
    saveDfToCsv(dfs.get("ALLOC"), "../output/portfolio_allocations.csv")
    print(f"\n{'[2]':<10}{' Portfolio performance ':*^70}")
    print(f"{'[2.1]':<10}{' Return ':*^70}")
    addReturn(dfs)
    for key, item in dfs.items(): showDf(key, item, 5, 10, False)
    print(f"{'[2.2]':<10}{' Volatility ':*^70}")
    addVolatility(dfs)
    for key, item in dfs.items(): showDf(key, item, 5, 10, False)
    saveDfToCsv(dfs.get("ALLOC"), "../output/portfolio_metrics.csv")

def cleanDf(df:pd.DataFrame) -> None:
    """! Cleans the DataFrame by removing unused columns & sets appropiate datatypes.

    @param df   The DataFrame to be modified.
    """
    df.drop(NON_USE_COLS_DS, inplace=True, axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Change %'] = df['Change %'].map(lambda x: x.rstrip('%'))
    df['Change %'] = df['Change %'].astype(str).astype(float)

def interpolateMissings(df:pd.DataFrame) -> pd.DataFrame:
    """! Finds missing dates and adds values to them based on existing line values.

    @param df   The DataFrame to be modified.
    @return The modified DataFrame, the new one.
    """
    modified = df.set_index('Date')
    missing = pd.date_range(start = START_DATE, end = END_DATE ).difference(modified.index)
    df = insertRows(modified, missing)
    df = df.reset_index()
    df = df.interpolate(method='ffill').interpolate(method='bfill')
    return df

def insertRows(df:pd.DataFrame, missing:pd.DataFrame):
  """! Add new rows to the DataFrame, corresponding to missing dates, and fill the columns with missing values (NaN).

  @param df   The DataFrame with dates as indexes.
  @param missing   The DataFrame with missing dates.
  @return The modified DataFrame, the new one.
  """
  df_result = df
  for row_number in missing:
    # Slice the upper half of the dataframe
    df1 = df_result[:row_number]
    # Store the result of lower half of the dataframe
    df2 = df_result[row_number:]
    # Insert the row in the upper half dataframe
    df1.loc[row_number] = np.nan
    # Concat the two dataframes
    df_result = pd.concat([df1, df2])
  # Return the updated dataframe
  return df_result

def allocPortDf(df:pd.DataFrame) -> None:
    """! Make the allocation in the DataFrame taking into account the characteristics of the statement (20% margins).

    @param df The DataFrame to be modified.
    """
    arr = [0,20,40,60,80,100]
    for subset in product(arr, repeat = 5):
        if sum(subset)==100:
            df.loc[len(df)] = list(subset)

def addReturn(dfs:dict) -> None:
    """! Calculates the return value for the different portfolios and adds them to the allocation DataFrame.

    @param dfs The dictionary with all the DataFrames.
    """
    df = dfs.get("ALLOC")
    for index, row in df.iterrows():
        buy = 0
        curr = 0
        for asset in ASSETS:
            lcdf = dfs.get("DF" + asset)
            # [Buy amount]
            buy = buy + (row[asset] * lcdf.loc[lcdf['Date'] == START_DATE]['Price'].item())
            # [Current value]
            curr = curr + (row[asset] * lcdf.loc[lcdf['Date'] == END_DATE]['Price'].item())
        # [Return value]
        retval = ((curr - buy) / buy) * 100
        df.loc[index,'RETURN'] = retval

def addVolatility(dfs:dict) -> None:
    """! Calculates the volatility value for the different portfolios and adds them to the allocation DataFrame.

    @param dfs The dictionary with all the DataFrames.
    """
    df = dfs.get("ALLOC")
    for index, row in df.iterrows():
        # [Get values]
        values = pd.Series([], dtype="float64")
        for asset in ASSETS:
            lcdf = dfs.get("DF" + asset)
            if row[asset] != 0: values = values.append((row[asset] * lcdf.loc[(lcdf['Date'] >= START_DATE) & (lcdf['Date'] <= END_DATE)]['Price']), ignore_index=True)
        # [Mean & Deviation]
        vlmean = values.mean()
        vlstdev = math.sqrt((values.apply(lambda v: pow((v - vlmean), 2))).sum() / len(values))
        # # [Volatility value]
        volatility = ((vlstdev / vlmean) * 100) if vlmean != 0 else 0
        df.loc[index,'VOLAT'] = volatility

def showDf(name:str, df:pd.DataFrame, rownum:int, padding:int, details:bool) -> None:
    """! Prints the DataFrame on a proper way (PrettyPrint).

    @param name    The name of the dataframe.
    @param df      The DataFrame object to be printed.
    @param rownum  The number of rows from DataFrame to be printed.
    @param padding The amount of space to the left before printing the DataFrame.
    @param details If details should be printed aswell (datatypes of columns).
    """
    newline = f"\n"
    empty = ""
    print(f"{newline}{empty:{padding}}[Name: {name}]")
    print(f"{newline.join(str(f'{empty:{padding}}') + l for l in df.head(rownum).to_string().splitlines())}")
    if details: print(f"\n{newline.join(str(f'{empty:{padding}}') + l for l in df.dtypes.to_string().splitlines())}")

def saveDfToCsv(df:pd.DataFrame, path:str) -> None:
    """! Save the DataFrame in a csv file.

    @param df The DataFrame to be saved.
    @param path The path were the file should be stored
    """
    with open(path, "w") as f: df.to_csv(f)

if __name__ == "__main__":
    main()