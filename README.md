# Programming-final-project
This repository stores the code corresponding to the final project corresponding to the subject *Programming for Data Science*. Likewise, the project has been developed by group number 5, whose members are detailed below. The repository is made up of several directories, the contents of each of which are described in the following table. 

| Directorio | Descripción |
| ---------- | ----------- |
| ./ | The main directory contains the other subdirectories shown below, as well as the *Doxygen* documentation generation configuration file (called *Doxyfile*) and this *README* file. |
| data   | This directory stores the data files (in CSV format) generated from the execution of the code corresponding to the first part of the project (web scraping). |
| driver   | This directory stores the driver necessary to carry out the web scraping tasks of the first section of the project. As explained below, it is only used for certain versions, so if necessary, it would be necessary to download another one for the correct functioning of the programme. |
| html | Here is the documentation generated from *Doxygen*. By using comments throughout the program code, documentation is generated in *HTML* format. To consult this documentation, simply run or open the file [index.html](./html/index.html) in a web browser. |
| output | In this directory you can find the files generated (also in CSV format) from the execution of the code corresponding to the second part of the project. The results of the analysis of the different investment strategies. |
| plots | In this directory you can find stored the images generated from the graphics obtained through the code corresponding to section three of the project. They have been stored in png format. |
| src | This directory contains all the *Python* code generated during the project, separated into different files according to their function (more details will be given in later sections). |

## Code execution
The project is divided into 3 main parts: web scraping, data generation and data analysis. The following shows how each of them should be carried out individually.

### Web scraping
This part performs the harvesting of historical data from investing.com for the following assets: *Amundi Index Msci World Ae-c*, *iShares Global Corporate Bond UCITS (CRPS)*, *Xtrackers II Global Government Bond UCITS ETF 5C (XG7S)*, *SPDR® Gold Shares (GLD)* and *US Dollar Index (DXY)*. The data harvested is stored in individual CSV files.

In order to be able to execute the code corresponding to this section, it is necessary, first of all, to have the web browser *Google Chrome* installed on the computer (as it is the one used to perform the web scrapping tasks). In addition, it is also necessary to have the corresponding ChromeDriver installed, which can be obtained from the following [link](https://chromedriver.chromium.org/downloads). Once the download is done, it is necessary to store the executable in the *driver/* directory of the repository with the following name: *chromedriver.exe*. The versions of web browser, driver and hardware features used for the execution of this section are shown below. So, if they match those of your machine, you do not need to make any changes.

- Google Chrome - version: 100.0.4896.127 (64 bits)
- ChromeDriver - version: 100.0.4896.60, so: Windows (64 bits)
 
Finally, the *Python* libraries needed are: 

- selenium - version: 4.1.3
- pandas - version: 1.4.2

Once the above requirements are fulfilled, to carry out the web scraping, just execute the following command from the src directory: python webscraping.py.

### Data generation
This part generates the files corresponding to the allocation of the different portfolios and the generation of different indices (return & volatility) for each one of them. 

First of all, in order to execute the code related to this section, it is necessary to have executed the code corresponding to the *Web scraping* section (since it is there where the files used as input for this section are generated), and also, to have the following *Python* libraries installed. The versions shown next to the libraries are the ones used by the group, and with which the code has been tested to work, although other versions may also work correctly.

- pandas - version: 1.4.2
- numpy - version: 1.22.1

Once the above requirements are fulfilled, to carry out the data generation, just execute the following command from the **src** directory: *python strategy.py*.

### Data analysis

The code in this section generates the necessary visualisation tools, created from the results obtained from the second part, in order to carry out the analysis of the different investment strategies.

As in the previous case, for the code developed for this section to work, it is necessary to have executed the code corresponding to the previous parts, or, on the contrary, to have the results files of the second section. The latter are used as data source in this third and last section. In addition, for a correct execution, the libraries shown below must be installed. The versions shown are those used in the development and testing of the programme, so if other versions are used, there could be conflicts.

- pandas - version: 1.4.2
- matplotlib - version: 3.3.4
- seaborn - version: 0.11.1

Once the above requirements are fulfilled, to carry out the data generation, just execute the following command from the **src** directory: *python analysis.py*.


## Group 5 members
The members of Group 5 are shown below.

- Sánchez Martinez, **Júlia**
- Longares Diez, **Ricardo María**
- Campoy Heredero, **Javier**
- Ayuso Luengo, **María**
- Amezua Lasuen, **Gorka**
