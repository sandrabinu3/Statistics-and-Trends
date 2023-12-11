
# importing the required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
from scipy.stats import kurtosis


def readFile(filename, cntry_list, indicator):
    """ function to read and clean a World Bank file

    Args:
        filename (string): filepath to the World Bank file
        cntry_list (list): list of selected Countries
        indicator (string): indicator selected

    Returns:
        final_df (dataframe): clean dataframe of selected indicator in
            selected countries for selected years having years as columns
        trans_df (dataframe): transposed dataframe of final_df having
                            countries as columns
    """
    df = pd.read_csv(filename, skiprows=2, header=1)  # read the data
    # filtering the data with country and indicators
    ref_df = df[(df['Country Name'].isin(cntry_list))
                & (df['Indicator Name'] == indicator)]
    # dropping the unwanted columns
    ref_df = ref_df.drop(df.columns[1:4], axis=1)
    ref_df = ref_df.drop(df.columns[-1:], axis=1)
    # filtering the years
    yr = [str(year) for year in range(1960, 2005)] + [str(year)
                                                      for year in range(2015, 2023)]
    final_df = ref_df.drop(columns=yr)
    # reseting the index
    final_df = final_df.reset_index(drop=True)
    # getting the transposed dataframe
    trans_df = final_df.transpose()
    # cleaning the transposed dataframe
    trans_df.columns = trans_df.iloc[0]
    trans_df = trans_df[1:]
    trans_df.index.names = ['Years']
    # returning the 2 dataframes
    return final_df, trans_df


def Corr_Heatmap(year):
    """ create a heatmap for selected indicators in a year

    Args:
        year (string): _selected year
    """
    # filtering out the required year from selected indicators
    renewop_lst = renew_op[year]
    ele_cons_lst = ele_cons[year]
    pop_tot_lst = pop_tot[year]
    access_tot_lst = access_tot[year]
    # making a dictionary of filtered values
    heat = {'Country Name': cntry_list,
            'Population_Total': pop_tot_lst,
            'Renewable_Output': renewop_lst,
            'Electricity_Consumption': ele_cons_lst,
            'Access_to_Electricity': access_tot_lst}
    # new filtered dataframe
    heat_df = pd.DataFrame(heat)
    # finding the corrilation between variables(corrilation matrix)
    corr_heat = heat_df.iloc[0:, 1:].corr()
    # plotting the heatmap using seaborn
    plt.figure(figsize=(8,6))
    sns.heatmap(corr_heat, annot=True, cmap='coolwarm', fmt=".2f",
                linewidths=0.5)
    # giving title to plot
    plt.title('Correlation Matrix of selected Indicators in 2014')
    # save the plot
    plt.savefig('Heatmap.png')
    # show the plot
    plt.show()


def Barplot(data, bar_width=0.1):
    """ create a stacked barplot for selected 
    countries for a selected indicator over years

    Args:
        data (dataframe): dataframe of selected indicator
        bar_width (float): Defaults to 0.1.
    """
    plt.figure()  # plot the bar plot
    plt.grid()  # giving grid to the plot
    # set the x and y axis values and stacked bars
    x = data['Country Name']
    y1 = data['2006']
    y2 = data['2008']
    y3 = data['2010']
    y4 = data['2012']
    y5 = data['2014']
    r1 = range(len(x))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
    r5 = [x + bar_width for x in r4]
    # draw the stacked bars
    plt.bar(r1, y1, color='b', width=bar_width)
    plt.bar(r2, y2, color='r', width=bar_width)
    plt.bar(r3, y3, color='g', width=bar_width)
    plt.bar(r4, y4, color='y', width=bar_width)
    plt.bar(r5, y5, color='c', width=bar_width)
    # define and label the axes
    plt.xticks([r + bar_width for r in range(len(x))], x)
    plt.legend(['2006', '2008', '2010', '2012', '2014'])
    plt.xlabel('Country')
    plt.ylabel('Electricity Consumption in KWh')
    plt.title('Electric Power Consumption')
    plt.savefig('Boxplot.png')
    plt.show()


def TimeSeries(country):
    """create a lineplot to know the timseries 
       change in the given indicators

    Args:
        country (string): country whose line plot should be known
    """
    # filtering the required countries from needed dfs as lists
    tot_lst = list(access_tot[access_tot['Country Name']
                   == country].iloc[0:, 1:].values[0])
    urban_lst = list(
        access_urban[access_urban['Country Name'] == country].iloc[0:, 1:].values[0])
    rural_lst = list(
        access_rural[access_rural['Country Name'] == country].iloc[0:, 1:].values[0])
    # creating a dictionary with filtered values
    df_dict = {'Years': list(np.arange(2005, 2015)),
               'Total': tot_lst,
               'Urban': urban_lst,
               'Rural': rural_lst}
    # making the filtered dataframe
    df = pd.DataFrame(df_dict)

    # plot the line chart
    plt.figure(figsize=(10, 6))
    plt.grid()
    # draw 3 lines corresponding to the 3 indicators
    plt.plot(df['Years'], df['Total'], label='Access% in total population',
             linestyle='--', marker='o')
    plt.plot(df['Years'], df['Urban'], label='Access% in total Urban population',
             linestyle='--', marker='o')
    plt.plot(df['Years'], df['Rural'], label='Access% in total Rural population',
             linestyle='--', marker='o')
    # labeling and limiting the axes
    plt.title('Access to Electricity from 2005-2014 in Malaysia')
    plt.xlabel('Years')
    plt.ylabel('Access to Electricity(%)')
    plt.xlim(2005, 2014)
    plt.ylim(97.5, 100)
    plt.legend()
    # save the figure
    plt.savefig('Lineplot.png')
    plt.show()


def Boxplot(data):
    """ createa boxplot for finding the spread of distribution

    Args:
        data (dataframe): data whose spread should be found
    """
    plt.figure()
    # plot the box plot using seaborn
    sns.boxplot(data)
    # labeling and saving the figure
    plt.title('Spread of Renewable Electricity o/p (2005-2014)')
    plt.ylabel('Renewable electricity output')
    plt.xlabel('Country')
    plt.savefig('Boxplot.png')
    plt.show()


def Pieplot(country, year):
    """ Create a pieplot for the distribution
        of electricity production sources

    Args:
        country ( string ): country whose production sources to be known
        year (string): year selected
    """
    # filtering the sources dfs for selected country and year
    lst = []
    for df in source_list:
        a = df[df['Country Name'] == country][str(year)].unique()[0]
        lst.append(a)
    # defining a list of source names
    src_list = ['Oil', 'Nuclear', 'Natural Gas',
                'Hydroelectric', 'Other Renewable', 'Coal']
    # plotting the piechart
    plt.figure()
    plt.pie(lst, labels=src_list, autopct='%1.1f%%', startangle=90,
            pctdistance=0.8, explode=(0, 0.12, 0, 0, 0, 0.08),
            wedgeprops={"edgecolor": "white", "linewidth": 2,
                        "antialiased": True})
    # labeling and saving the figure
    plt.title('Electricity production from Different Sources in Brazil')
    plt.savefig('Pieplot.png')
    plt.show()


def Distplot(country):
    """ create a Distribution plot to see the distribution of data and 
    also to mark its skewness and kurtosis

    Args:
        country (string): country whose distribution 
        on selected indicator should be found
    """
    # filtering the indicator with selected country
    country_df = renew_op.loc[renew_op['Country Name'] == country]
    # melting the df to create a new one with desire
    country_melt = pd.melt(country_df, id_vars=[
                           'Country Name'], var_name='Year', value_name='Value')
    # filter the numerical values of the country out
    country_filt = country_df.iloc[:, 1:].values.flatten()
    # plot the figure
    plt.figure(figsize=(8, 6))
    sns.set(style="whitegrid")
    # draw the distribution plot using seaborn
    sns.distplot(country_melt['Value'], bins=10,
                 hist=True, kde=True, color='green')
    # finding skewness and kurtosis and labeling them in plot using plt.text()
    plt.text(x=65, y=0.175, s='Skewness: ' +
             f'{np.round(skew(country_filt),2)}', color="red", fontsize=12)
    plt.text(x=65, y=0.160, s='Kurtosis: ' +
             f'{np.round(kurtosis(country_filt),2)}', color="red", fontsize=12)
    # labeling and saving the plot
    plt.title('Distribution of Renewable Electricity o/p for Brazil (2005-2014)')
    plt.xlabel('Renewable Electricity output(% of total)')
    plt.ylabel('Density')
    plt.savefig('Distplot.png')
    plt.show()


# defining the filepaths
climate = "API_19_DS2_en_csv_v2_6183479.csv"
ele_rural = "API_EG.ELC.ACCS.RU.ZS_DS2_en_csv_v2_5995527.csv"
ele_urban = "API_EG.ELC.ACCS.UR.ZS_DS2_en_csv_v2_5995527.csv"

# selecting the needed countries for study
cntry_list = ['Brazil', 'Argentina', 'Poland', 'China', 'Malaysia']

# reading and filtering dataframes of selected indicators
pop_tot, pop_tot_trans = readFile(climate, cntry_list, 'Population, total')
renew_op, renew_op_trans = readFile(
    climate, cntry_list, 'Renewable electricity output (% of total electricity output)')
oil, oil_trans = readFile(
    climate, cntry_list, 'Electricity production from oil sources (% of total)')
nuclear, nuclear_trans = readFile(
    climate, cntry_list, 'Electricity production from nuclear sources (% of total)')
gas, gas_trans = readFile(
    climate, cntry_list, 'Electricity production from natural gas sources (% of total)')
hydro, hydro_trans = readFile(
    climate, cntry_list, 'Electricity production from hydroelectric sources (% of total)')
coal, coal_trans = readFile(
    climate, cntry_list, 'Electricity production from coal sources (% of total)')
access_tot, access_tot_trans = readFile(
    climate, cntry_list, 'Access to electricity (% of population)')
access_urban, access_urban_trans = readFile(
    ele_urban, cntry_list, 'Access to electricity, urban (% of urban population)')
access_rural, access_rural_trans = readFile(
    ele_rural, cntry_list, 'Access to electricity, rural (% of rural population)')
renew, renew_trans = readFile(
    climate, cntry_list, 'Electricity production from renewable sources, excluding hydroelectric (% of total)')
ele_cons, ele_cons_trans = readFile(
    climate, cntry_list, 'Electric power consumption (kWh per capita)')

# list of dataframes of sources for electricity production
source_list = [oil, nuclear, gas, hydro, renew, coal]

# gives the statistical description of the dataframe
#calculate statistical properties of total access%
access_tot_describe=access_tot.describe()

#calculate the mean urban and rural access% of selected countries in 2005 and 2014
urb_05=np.round(access_urban['2005'].mean(),2)
urb_14=np.round(access_urban['2014'].mean(),2)
rur_05=np.round(access_rural['2005'].mean(),2)
rur_14=np.round(access_rural['2014'].mean(),2)

''' heatmap showing the correlation between selected indicators'''
Corr_Heatmap('2014')

'''create a stacked barplot for electricity consumption 
   in selected countries over selected years '''
Barplot(ele_cons, bar_width=0.1)

'''lineplot showing access% of total urban and rural to electricity'''
TimeSeries('Malaysia')

''' boxplot of selected countries' electrcity consumption'''
Boxplot(renew_op_trans)

''' pieplot of brazil showing its electricity production sources'''
Pieplot('Brazil', '2014')

''' Distribution plot to see the distribution of renewable 
    electricity o/p of Brazil over years '''
Distplot('Brazil')
