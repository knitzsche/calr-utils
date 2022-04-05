#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []

data1 = dict() # key is column header, val is col data list
data2 = dict() # key is column header, val is col data list

def help():
    print("Description:")
    print("    The program creates a new CalR CSV file that contains the specified subject IDs' data columns.")
    print("    Two input CalR CSV files are required.")
    print("    Input CalR files must have column headers in this format: testname_subjectID.")
    print("        For example: 'allmeters_14L20NA,allmeters_15L20NA,pedmeters_16L20NA,'")
    print("        Where the tests from that are 'allmeters', and 'pedmeters'.") 
    print("        Where the subject IDs from that are '14L20NA', '15L20NA' and '16L20NA'") 
    print("Four args are required:")
    print("    Args 1, 2: Input CalrR CSV files that contain data columns for the desired test_subjectID")
    print("    Arg 3: Subject IDs you want included. Put them inside quote marks and delimit with commas:")
    print("        Example: \"L5A,L10A,L15A\"")
    print("    Arg4: The created calr file.")

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()
        sys.exit()
    if len(sys.argv) < 5:
        help()
        sys.exit(1)

    print("1: ", sys.argv[1])
    print("2: ", sys.argv[2])
    print("3: ", sys.argv[3])
    print("4: ", sys.argv[4])
    #sys.exit()
    out_file = sys.argv[4]

    with open(sys.argv[1], newline='') as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            i= i+1
            if i == 0: #first row: column headers
                top1=row
                for col in top1:
                    data1[col]=list()
                continue
            i2 = -1
            for col in row:
                i2 = i2+1
                data1[top1[i2]].append(col)


    with open(sys.argv[2], newline='') as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            i= i+1
            if i == 0: #first row: column headers
                top2=row
                for col in top2:
                    data2[col]=list()
                continue
            i2 = -1
            for col in row:
                i2 = i2+1
                data2[top2[i2]].append(col)

    data = dict()
    data.update(data1)
    data.update(data2)

    # the CalR subject IDs
    subject_ids = sys.argv[3].split(",")

    lines = []
    matched = []
    num_cols = len(data.keys())
    line = ''

    #make first line from matching keys
    for k in data:
        for sub in subject_ids:
            if k.endswith(sub): #the CalR column header ends with a target subject ID
                matched.append(k)
                line += k+","
    lines.append(line)
    line = ''
   
    # add data
    idx = -1
    num_out_of_data = 0 # tracks the number of matched lists that are fully processed
    # when num_of_data = len(matched), done: quit looping
    while True:
        #print(idx, num_out_of_data, len(matched)) 
        if num_out_of_data == len(matched): break
        idx = idx+ 1
        for k in matched:
            if len(data[k]) >= idx + 1:
                line += data[k][idx] + ","
                continue
            else:
                #print('sub: {} num_out_of_data {}'.format(k, num_out_of_data))
                num_out_of_data += 1
        lines.append(line)
        line = ''
                    
    lines_final = []
    #remove trailing comma on each line
    for line in lines:
        lines_final.append(line[:-1])
    f = open(out_file, 'w')
    for line in lines_final:
        f.write(line)
        f.write("\n")
    f.flush()
    f.close()
    sys.exit()
