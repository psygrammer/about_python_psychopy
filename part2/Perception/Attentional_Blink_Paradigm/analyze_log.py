# -*- coding: utf-8 -*-

import csv
import numpy as np
import matplotlib.pyplot as plt

# TODO any title for the graph
# TODO test different csv forms; now it works only with commas
# TODO stats for scatter? fit and parameters?

# Changelog
# 2013.07.12.   filt_cond bugfix;
# 2013.06.22.   sort groups; label groups; bar fixes;
# 2013.06.18.   filt_cond; graph_type => graph_types;
#               set the parameters from terminal if run as main
# 2013.05.17.   scatterplot
# 2013.05.11.   first version

def mean(number_list):
    if len(number_list) == 0:
        return float('nan')
    return sum(number_list) / len(number_list)

def median(number_list):
    if len(number_list) == 0:
        return float('nan')
    return np.median(np.array(number_list))


def analyze_log (filename='', indep_var=None, dep_var=None, function='mean', filt_cond='', print_results = True, write_results = True, output_file='', display_graph = True, graph_types=['boxplot']):
    """
    === Data to analyze ===
    filename: File to analyze
        File should be a csv file, comma separated. First line should include the variable names.
        Variables are identified by their names in the header of the csv file.

    === Variables and functions ===
    indep_var: Group the data with this variable
        At the moment it can be only a single variable (no multiple independent variables).
    dep_var: Dependent variable
    function: simple statistics function
        It can be 'mean' or 'median' at the moment.
        Default is 'mean'.
    filt_cond: expression describing filtering condition
        Names of the variables can be used in Python expression
        Name of the variables should be between $ signs, e.g. $error$

    === Display results ===
    print_results: Print the results to the console?
        Default is True
    write_results: Write the results to a file?
        Default is True.
    output_file: Filename to write the results to.
        Default is filename + results.txt
    display_graph: Display the results as a graph?
        Default is True
    graph_types: List of type of the graphs.
        'boxlplot' draws boxplot.
        'bar' draws bar chart with thegiven statistics function.
        'line' draws line chart with thegiven statistics function.
        'scatter' draws scatterplot.
        Default is 'boxplot'.
        You can use several graphs in the same graph. It is useful to display raw data and statistics.

    If you run the module directly, it asks for the parameters on the terminal.
        
    Example:
    analyze_log (filename='participant_name_symb_comp.csv',
                             indep_var='distance', dep_var='RT', function='median', filt_cond='$error$==0',
                             print_results = True, write_results = True, display_graph = True, 
                             graph_types=['boxplot', 'line'])
    """
    
    if filename == '':
        print 'File name was not given. No analysis is run.'
        return
    # TODO check if file exists
    var_names = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            if not var_names:
                var_names = row
                log_data = [[] for i in var_names]
            else:
                for i, data in enumerate(row):
                    try:
                        log_data[i].append(float(data))
                    except:
                        log_data[i].append(data)
    #print var_names, log_data

#    from IPython import embed
#    embed()

    # Filter the data if necessary
    if filt_cond:
        # Swap variable names in expression to reference to the variable
        for var_name in var_names:
            filt_cond = filt_cond.replace('$'+var_name+'$', "x[var_names.index('"+var_name+"')]")
        #print filt_cond
        filt_rows = [True if eval(filt_cond) else False for x in map(list, zip(*log_data)) ]
        if len(filt_rows)==0:
            print 'Filtered data is empty!'
            return
    else: # All data will be used
        filt_rows = [True for x in log_data[0]]
    #print 'Rows to fiter: ', filt_rows
    
    # Group the data
    if indep_var:
        groups = list(set(log_data[var_names.index(indep_var)]))
        groups.sort() # TODO is it OK to sort the groups?
        grouped_data = [[] for i in groups]
        for group_i, group in enumerate(groups):
            grouped_data[group_i] = [data for data, group_data, filt_row in zip(log_data[var_names.index(dep_var)], log_data[var_names.index(indep_var)], filt_rows)  if group_data == group and filt_row]
    else:
        groups = ['all data']
        grouped_data = [log_data[dep_var]]
    
    # Compute the statistics
    if write_results:
        if output_file == '':
            output_file = filename+'_result.txt'
        out_file = open(output_file, 'a')
        out_file.write('independent: %s, dependent: %s, filter: %s \ngroup, n, %s\n' %(indep_var, dep_var, filt_cond, function)) # Header
    if print_results: print 'independent: %s, dependent: %s, filter: %s \ngroup, n, %s' %(indep_var, dep_var, filt_cond, function) # Header
    for group, data in zip(groups, grouped_data):
        result = eval(function+'(data)')
        if print_results: print '%s, %d, %f' %(group, len(data), result)
        if write_results: out_file.write('%s, %d, %f\n' %(group, len(data), result))

    # Display the graph
    if display_graph:
        for graph_type in graph_types:
            if graph_type == 'boxplot':
                plt.boxplot(grouped_data)
            elif graph_type == 'bar':
                plt.bar(np.arange(len(groups))+0.8, [eval(function+'(grouped_data[i])') for i in range(len(groups))], 0.4, color='#aaffaa')
            elif graph_type == 'line':
                plt.plot(np.arange(len(groups))+1, [eval(function+'(grouped_data[i])') for i in range(len(groups))], '-')
            elif graph_type == 'scatter':
                plt.plot(log_data[var_names.index(indep_var)], log_data[var_names.index(dep_var)], 'o')
            else:
                print 'Invalid graph_type'
        plt.xlabel(indep_var)
        plt.ylabel(dep_var)
        plt.xticks(range(1,len(groups)+1), groups)
        plt.show()

if __name__ == '__main__':
    # Tests
#    analyze_log (filename='participant_ID_dot_comparison.csv', 
#                 indep_var='test_n', dep_var='test_larger', function='mean',
#                 graph_types=['line'])
#    analyze_log (filename='participant_ID_qp_parity.csv',
#                         indep_var='number', dep_var='RT', function='mean', filt_cond = '$error$==0',
#                         graph_types=['boxplot', 'line'])
#    analyze_log (filename='participant_ID_dot_enum.csv',
#                         indep_var='num2', dep_var='RT', function='median', filt_cond = '$error$==0',
#                         graph_types=['boxplot', 'line'])
#    analyze_log (filename='participant_name_symb_comp.csv',
#                 indep_var='distance', dep_var='RT', function='median', filt_cond='$error$==0',
#                 print_results = True, write_results = True, display_graph = True, 
#                 graph_types=['boxplot', 'line'])
                 
    # Set the parameters from terminal
    while True:
        filename = raw_input('What is the name of the file? ')
        try:
            csvfile = csv.reader(open(filename), skipinitialspace=True)
            var_names = csvfile.next()
            print 'Available variables:', var_names
            break
        except:
            print "Couldn't find the file. Type it again."
    while True:
        indep_var = raw_input('What is the independent variable? ')
        if indep_var in var_names: break
        else:
            print "Couldn't find this variable in that file. Type it again."
    while True:
        dep_var = raw_input('What is the dependent variable? ')
        if dep_var in var_names: break
        else:
            print "Couldn't find this variable in that file. Type it again."
    # TODO check these stuffs if possible
    function = raw_input('What function do you want to use? ')
    filt_cond = raw_input('What filter condition do you want to use? ')
    graph_types= raw_input('What graph_types do you want to use? ')
    analyze_log (filename=filename,
                 indep_var=indep_var, dep_var=dep_var, function=function, filt_cond=filt_cond,
                 print_results = True, write_results = True, display_graph = True, 
                 graph_types=[graph_types])
