#Write code that goes through exp1, subexp1, subexp2, subexp3, and subexp4 and for each subexp it goes through pur8.log, pur32.log, pur128.log, pur512.log, and pur2048.log and extracts the time taken to read the files and time taken by compute part of function.
#The format of the log files is as follows:
# Time taken to read the files: 181 microseconds
# Time taken by compute part of the function: 318 microseconds
#....
#By extracting these number from each pur*.log file, you should have 2 arrays of data. One for time taken to read the files and one for time taken by compute part of the function. You should then plot these arrays using matplotlib. The x-axis should be the size of the file (8, 32, 128, 512, 2048) and the y-axis should be the time taken in microseconds. You should have 2 lines on the graph, one for time taken to read the files and one for time taken by compute part of the function. The graph should have a title, x-axis label, y-axis label, and a legend. The title should be "Time taken to read files and compute part of function vs file size". The x-axis label should be "Purchase size" and the y-axis label should be "Time taken in microseconds". The legend should have "Time taken to read files" and "Time taken by compute part of function". The graph should be saved as a png file called "graphsubexp1.png".
#Go through each subexp to generate a graph for each subexp. The graph should be saved as a png file called "graphsubexp*.png" where * is the number of the subexp.

import matplotlib.pyplot as plt
import os
import re

def extract_data(file):
    #Input is the file name which is exp1/subexp1/pur
    #iterate through the files pur8.log, pur32.log, pur128.log, pur512.log, pur2048.log
    #extract the time taken to read the files and time taken by compute part of the function
    #return the two arrays
    read_time = []
    compute_time = []
    for i in [8, 32, 128, 512, 2048]:
        with open(f'{file}{i}.log', 'r') as f:
            lines = f.readlines()
            read_time.append(int(re.search(r'\d+', lines[0]).group()))
            compute_time.append(int(re.search(r'\d+', lines[1]).group()))
    return read_time, compute_time


def graph_data(read_time, compute_time, file):
    x = [8, 32, 128, 512, 2048]
    plt.plot(x, read_time, label='Time taken to read files')
    plt.plot(x, compute_time, label='Time taken by compute part of function')
    plt.title('Time taken to read files and compute part of function vs file size')
    plt.xlabel('Purchase size')
    plt.ylabel('Time taken in microseconds')
    plt.legend()
    plt.savefig(file)
    plt.close()

def main():
    #The files are stored in exp1\subexp1, exp1\subexp2, exp1\subexp3, and exp1\subexp4
    for i in range(1, 5):
        read_time, compute_time = extract_data(f'exp1/subexp{i}/pur')    
        graph_data(read_time, compute_time, f'exp1graphsubexp{i}.png')

if __name__ == '__main__':
    main()