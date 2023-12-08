
# importing the required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
    df = pd.read_csv(filename, skiprows=2, header=1)
    ref_df = df[(df['Country Name'].isin(cntry_list))
                & (df['Indicator Name'] == indicator)]
    ref_df = ref_df.drop(df.columns[1:4], axis=1)
    ref_df = ref_df.drop(df.columns[-1:], axis=1)
    yr = [str(year) for year in range(1960, 2005)] + [str(year)
                                                      for year in range(2015, 2023)]
    final_df = ref_df.drop(columns=yr)
    final_df = final_df.reset_index(drop=True)
    trans_df = final_df.transpose()
    trans_df.columns = trans_df.iloc[0]
    trans_df = trans_df[1:]
    trans_df.index.names = ['Years']
    return final_df, trans_df


def Barplot(data, bar_width=0.1):
    """ create a stacked barplot for selected 
    countries for a selected indicator over years

    Args:
        data (dataframe): dataframe of selected indicator
        bar_width (float): Defaults to 0.1.
    """
    plt.figure(0)
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
    r5 = [x+bar_width for x in r4]
    plt.bar(r1, y1, color='b', width=bar_width)
    plt.bar(r2, y2, color='r', width=bar_width)
    plt.bar(r3, y3, color='g', width=bar_width)
    plt.bar(r4, y4, color='y', width=bar_width)
    plt.bar(r5, y5, color='c', width=bar_width)
    plt.grid()
    plt.xticks([r + bar_width for r in range(len(x))], x)
    plt.legend(['2006', '2008', '2010', '2012', '2014'])
    plt.xlabel('Countries')
    plt.ylabel('Electricity Consumption in KWh')
    plt.title('Electric Power Consumption')
    plt.savefig('Boxplot.png')
    plt.show()


def Pieplot(country, year):
    """ Create a pieplot for the distribution
        of electricity production sources

    Args:
        country ( string_): country whose production sources to be known
        year (_string_): year selected
    """
    lst = []
    for i in pro_list:
        a = i[i['Country Name'] == country][str(year)].unique()[0]
        lst.append(a)
    src_list = ['Oil', 'Nuclear', 'Natural Gas',
                'Hydroelectric', 'Other Renewable', 'Coal']
    plt.figure()
    plt.pie(lst, labels=src_list, autopct='%1.1f%%', startangle=90,
            pctdistance=0.8, explode=(0, 0.1, 0, 0, 0, 0.08), wedgeprops={"edgecolor": "black", "linewidth": 2,
                                                                          "antialiased": True})
    plt.title('Electricity production from Different Sources')
    plt.savefig('Pieplot.png')
    plt.show()


def TimeSeries(country):
    """create a lineplot to know the timseries 
       change in the given indicators

    Args:
        country (string): country whose line plot should be known
    """
    tot_lst = list(access_tot[access_tot['Country Name']
                   == country].iloc[0:, 1:].values[0])
    urban_lst = list(
        access_urban[access_urban['Country Name'] == country].iloc[0:, 1:].values[0])
    rural_lst = list(
        access_rural[access_rural['Country Name'] == country].iloc[0:, 1:].values[0])

    df_dict = {'Years': list(np.arange(2005, 2015)),
               'Total': tot_lst,
               'Urban': urban_lst,
               'Rural': rural_lst}
    df = pd.DataFrame(df_dict)

    plt.figure(figsize=(10, 6))
    sns.set_style('whitegrid')
    plt.plot(df['Years'], df['Total'], label='Access% in total population',
             linestyle='--', marker='o')
    plt.plot(df['Years'], df['Urban'], label='Access% in total Urban population',
             linestyle='--', marker='o')
    plt.plot(df['Years'], df['Rural'], label='Access% in total Rural population',
             linestyle='--', marker='o')
    plt.title('Access to Electricity from 2005-2014')
    plt.xlabel('Years')
    plt.ylabel('Access to Electricity(%)')
    plt.legend()
    plt.savefig('Lineplot.png')
    plt.show()


def Corr_Heatmap(year):
    """ create a heatmap for selected indicators in a year

    Args:
        year (string): _selected year
    """
    renewop_lst = renew_op[year]
    ele_cons_lst = ele_cons[year]
    pop_tot_lst = pop_tot[year]
    access_tot_lst = access_tot[year]
    heat = {'Country Name': cntry_list,
            'Population_Total': pop_tot_lst,
            'Renewable_Output': renewop_lst,
            'Electricity_Consumption': ele_cons_lst,
            'Access_to_Electricity(total)': access_tot_lst}
    heat_df = pd.DataFrame(heat)
    corr_heat = heat_df.iloc[0:, 1:].corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr_heat, annot=True, cmap='coolwarm',
                fmt=".2f", linewidths=.5)
    plt.title('Correlation Matrix of selected Indicators in 2014')
    plt.savefig('heatmap.png')
    plt.show()


def Boxplot(data):
    """ createa boxplot for finding the spread of distribution

    Args:
        data (dataframe): data whose spread should be found
    """
    plt.figure()
    sns.boxplot(data)
    plt.title('Electricity Consumption in Different Countries from 2005-2014')
    plt.ylabel('Electricity Consumption(KWh)')
    plt.savefig('Boxplot.png')
    plt.show()


climate = 'API_19_DS2_en_csv_v2_6183479.csv'
ele_rural = 'API_EG.ELC.ACCS.RU.ZS_DS2_en_csv_v2_5995527.csv'
ele_urban = 'API_EG.ELC.ACCS.UR.ZS_DS2_en_csv_v2_5995527.csv'

cntry_list = ['Brazil', 'Argentina', 'Poland', 'China', 'Malaysia']

ind = ['Population, total',
       'Renewable electricity output (% of total electricity output)',
       'Electricity production from oil sources (% of total)',
       'Electricity production from nuclear sources (% of total)',
       'Electricity production from natural gas sources (% of total)',
       'Electricity production from hydroelectric sources (% of total)',
       'Electricity production from coal sources (% of total)',
       'Access to electricity (% of population)',
       'Access to electricity, urban (% of urban population)',
       'Access to electricity, rural (% of rural population)'
       'Electricity production from renewable sources, excluding hydroelectric (% of total)',
       'Electric power consumption (kWh per capita)']

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


pro_list = [oil, nuclear, gas, hydro, renew, coal]

Barplot(ele_cons, bar_width=0.1)
Pieplot('Brazil', '2014')
TimeSeries('Malaysia')
Corr_Heatmap('2014')
Boxplot(ele_cons_trans)
