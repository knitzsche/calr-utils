#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []

data = dict() # key is column header, val is col data list

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
    print("    Arg 3: Common *ending* of subject IDs you want included. Put them inside quote marks and delimit with commas:")
    print("        Example: \"L5A,L10A,L15A\"")
    print("        Note: that is the *common ending* of subject IDs. Acutal IDs could be, for example \"1L5A,2L5A,4L15A... \"")
    print("    Arg4: The created CalR file. If this file exists, it is overwritten.")

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()
        sys.exit()
    #if len(sys.argv) < 5:
        #TODO help()
        #sys.exit(1)

    in_fs = sys.argv[1]
    g_ids = sys.argv[2]
    out_file = sys.argv[3]

    calrs = [] # the list of calr dictionaries from infiles

    # read all calrs on input into list of dicts
    for f in in_fs.split(','):
        rows = []
        with open(f, newline='') as f:
            i = -1
            reader = csv.DictReader(f)
            for row in reader: # dict with keys first row cell values
                i = i + 1
                rows.append(row)
        # convert my list of dicts into a dict of lists
        # key is header cell
        # value is a list of the column cells
        data.clear()
        i = -1
        for row in rows: # row is dict
            i = i + 1
            for key in row:
                if i == 0:
                    data[key] = [row[key]]
                else:
                    data[key].append(row[key])
        calrs.append(data.copy()) 

    #print(calrs[1].keys())
    sys.exit()

    # the CalR subject ID common endings
    subject_id_common_endings = sys.argv[3].split(",")

    # TODO check if desired columns have different lengths and if so, warn

    lines = []
    matched = []
    num_cols = len(data.keys())
    line = ''

    #make first line from matching keys
    for k in data:
        for sub in subject_id_common_endings:
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
