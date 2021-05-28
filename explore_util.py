# import needed packages
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# create function to explore numerical data
def explore_num_data(data, n):
    '''
    Function to explore numerical data
    
    param data: pandas dataframe
    param n: integer to determine the number of first and last values to return (when sorted) for each numerical variable
    
    returns: for each numerical variable a pandas dataframe which includes row count, number of distinct values, 5-number
             summary, mean, standard deviation, sum, percentage null, percentage zero, percentage positive, and percentage
             negative
             
             for each numerical variable a pandas dataframe which include the most frequent values, the first n values,
             and the last n values
    '''
    
    # create list of numerical columns
    columns = [i for i in (data.select_dtypes(include=['float64', 'int64']).columns)]
    
    # select numerical columns within dataframe
    data = data[columns]
    
    # call describe function to calculate count, mean, std, and 5-number summary
    describe_df = data.describe()
    
    # create list of number of distinct values within each numerical column
    dist_num = [len(data[i].dropna().unique()) for i in columns]
    
    # create list of the sum of all values within each numerical column
    total_sum = [data[i].sum() for i in columns]
    
    # calculate total number of rows
    total_count = len(data)
    
    # calculate percentage null for each numerical column
    null_perc = [100.0 * data[i].isna().sum() / total_count for i in columns]
    
    # calculate percentage zero for each numerical column
    zero_perc = [100.0 * len(data.loc[data[i] == 0, i]) / total_count for i in columns]
    
    # calculate percentage positive for each numerical column
    pos_perc = [100.0 * len(data.loc[data[i] > 0, i]) / total_count for i in columns]
    
    # calculate percentage negative for each numerical column
    neg_perc = [100.0 * len(data.loc[data[i] < 0, i]) / total_count for i in columns]
    
    # create temporary dataframe for statistics created above
    temp_df = pd.DataFrame({'dist_num': dist_num
                           ,'total_sum': total_sum
                           ,'null_perc': null_perc
                           ,'zero_perc': zero_perc
                           ,'pos_perc': pos_perc
                           ,'neg_perc': neg_perc
                           }).transpose()
    
    # set columns
    temp_df.columns = columns
    
    # concatenate describe_df and temp_df
    df = pd.concat([describe_df, temp_df], sort = False)
    
    # set index name
    df.index.set_names('summary', inplace = True)
    
    # transpose dataframe
    df = df.transpose()
    
    # reorder dataframe
    df = df[['count'
            ,'dist_num'
            ,'min'
            ,'25%'
            ,'50%'
            ,'75%'
            ,'max'
            ,'mean'
            ,'std'
            ,'total_sum'
            ,'null_perc'
            ,'zero_perc'
            ,'pos_perc'
            ,'neg_perc'
            ]]
    
    # rename count column
    df.rename(columns={'count':'row_count'}, inplace=True)
    
    # calculate most frequent values within each numerical column
    freq = []
    for i in columns:
        temp_freq = data.groupby(i).agg(count = (i, 'count')).sort_values('count', ascending = False).reset_index().head(n)
        temp_freq['freq'] = temp_freq['count'] / total_count
        freq.append(temp_freq)
    
    # calculate the first n values within each numerical column when sorted
    first_values = []
    for j in columns:
        temp_first_values = data.groupby(j).agg(count = (j, 'count')).sort_values(j, ascending = True).reset_index().head(n)
        temp_first_values['freq'] = temp_first_values['count'] / total_count
        first_values.append(temp_first_values)
    
    # calculate the last n values within each numerical column when sorted
    last_values = []
    for k in columns:
        temp_last_values = data.groupby(k).agg(count = (k, 'count')).sort_values(k, ascending = False).reset_index().head(n)
        temp_last_values['freq'] = temp_last_values['count'] / total_count
        last_values.append(temp_last_values)
    
    return df, freq, first_values, last_values
	
# create function to explore categorical data
def explore_cat_data(data, n):
    '''
    Function to explore categorical data
    
    param data: pandas dataframe
    param n: integer to determine the number of first and last values to return (when sorted) for each categorical variable
    
    returns: for each categorical variable a pandas dataframe which includes minimum string length, maximum string length, row count, number of 
             distince values, percent null, and percent empty
             
             for each categorical variable a pandas dataframe which include the most frequent values, the first n values,
             and the last n values
    '''
    
    # create list of categorical columns
    columns = [i for i in (data.select_dtypes(include=['string', 'object', 'category']).columns)]
    
    # select categorical columns within dataframe
    data = data[columns]
    
    # calculate row count
    count_rows = [data[i].dropna().count() for i in columns]
    
    # calculate number of distinct values
    dist_num = [data[i].dropna().value_counts().count() for i in columns]
    
    # calculate total number of rows
    total_count = len(data)
    
    # calculate minimum length for each categorical column
    min_length = [data[i].astype(str).str.len().min() for i in columns]
    
    # calculate maximum length for each categorical column
    max_length = [data[i].astype(str).str.len().max() for i in columns]
    
    # calculate percentage null for each categorical column
    null_perc = [100.0 * data[i].isna().sum() / total_count for i in columns]
    
    # calculate percentage empty for each categorical column
    empty_perc = [100.0 * len(data.loc[data[i] == '', i]) / total_count for i in columns]    
    
    # combine above stats into a pandas dataframe
    df = pd.DataFrame({'row_count': count_rows
                      ,'dist_num': dist_num
                      ,'min_length': min_length
                      ,'max_length': max_length
                      ,'null_perc': null_perc
                      ,'empty_perc': empty_perc
                      }).transpose()
					  
    # add column names
    df.columns = columns
    
    # calculate most frequent values within each categorical column
    freq = []
    for i in columns:
        temp_freq = data.groupby(i).agg(count = (i, 'count')).sort_values('count', ascending = False).reset_index().head(n)
        temp_freq['freq'] = temp_freq['count'] / total_count
        freq.append(temp_freq)
    
    # calculate the first n values within each categorical column when sorted
    first_values = []
    for j in columns:
        temp_first_values = data.groupby(j).agg(count = (j, 'count')).sort_values(j, ascending = True).reset_index().head(n)
        temp_first_values['freq'] = temp_first_values['count'] / total_count
        first_values.append(temp_first_values)
    
    # calculate the last n values within each categorical column when sorted
    last_values = []
    for k in columns:
        temp_last_values = data.groupby(k).agg(count = (k, 'count')).sort_values(k, ascending = False).reset_index().head(n)
        temp_last_values['freq'] = temp_last_values['count'] / total_count
        last_values.append(temp_last_values)
    
    return df, freq, first_values, last_values
	
# create function to plot histograms for each numerical variable
def plot_hist(data, file_name, output_dir):
    # create list of numerical columns
    columns = [i for i in (data.select_dtypes(include=['float64', 'int64']).columns)]
    
    # create pdf object
    pdf_obj = PdfPages(output_dir + '/{}_histograms.pdf'.format(file_name))
    
    # create histogram for each numerical variable
    for col in columns:
        f = plt.figure()
        plt.hist(data['{}'.format(col)].dropna(), bins = 50, color = 'green')
        plt.title('{}'.format(col))
        pdf_obj.savefig(f)
        plt.close()
    pdf_obj.close()

# create function to plot correlation matrix	
def corr_matrix(data, file_name, output_dir):
    columns = list(data.select_dtypes(include=['float64', 'int64']).columns)
    
    if len(columns) != 0:
        
        # create a correlation matrix for all numerical columns and export to csv
        corr = data.corr()
        
        # save to cvs
        corr.to_csv(output_dir + '/{}_correlation_analysis.csv'.format(file_name), index = True)
        
        # display heatmap if the columns are less than or equal 10, otherwise, the heatmap is too big to easily read within notebook
        if len(columns) <= 10:
            
            # create a correlation matrix with a heatmap and export to png
            fig, ax = plt.subplots(figsize = (8, 8))
            g = sns.heatmap(corr, annot = True, fmt = '.2f', cmap = plt.get_cmap('coolwarm'), cbar = False, ax = ax)
            plt.savefig(output_dir + '{}_correlation_analysis.png'.format(file_name), bbox_inches='tight', pad_inches=0.0)
    else: 
        print("no numerical columns")

# create function to run the exploration functions created above 		
def run_explore_func(data, func, func_var, positional_group, print_flag, output_dir):
    
    # run explore_num_data function
    df, freq_df_list, first_values_df_list, last_values_df_list = func(data, 5)

    # print or save to csv
    if print_flag:
        print("Summary:")
        display(df)
    else:
        df.to_csv(output_dir + f"/{positional_group}_{func_var}_data.csv")
        
    # print or save to csv
    if print_flag:
        print("Most Frequent Values:")
        for i in range(0, len(freq_df_list)):
            display(freq_df_list[i])
    else:
        freq_df = pd.DataFrame({f'{positional_group}_{func_var}_freq': freq_df_list}).to_csv(output_dir + f"/{positional_group}_{func_var}_freq.csv", index = False)
        
    # print or save to csv
    if print_flag:
        print("First 5 Values:")
        for j in range(0, len(first_values_df_list)):
            display(first_values_df_list[j])
    else:
        first_values_df = pd.DataFrame({f'{positional_group}_{func_var}_first_values': first_values_df_list}).to_csv(output_dir + f"/{positional_group}_{func_var}_first_values.csv", index = False)
        
    
    # print or save to csv
    if print_flag:
        print("Last 5 Values:")
        for k in range(0, len(last_values_df_list)):
            display(last_values_df_list[k])
    else:
        last_values_df = pd.DataFrame({f'{positional_group}_{func_var}_last_values': last_values_df_list}).to_csv(output_dir + f"/{positional_group}_{func_var}_last_values.csv", index = False)