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

    get_subject_ids = False
    if "subject_ids" in sys.argv:
        get_subject_ids = True

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
        # convert my per calr list of dicts into a dict of lists
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

    print(calrs[1]['vo2_1L10A'])
    x#sys.exit()

    # get the CalR subject Is'D common endings: that is, group IDs
    group_ids = g_ids.split(",")
    #print(group_ids)

    rows.clear()
    subject_ids = []
    for calr in calrs:
        for g_id in group_ids:
            row = []
            i = -1
            for key in calr:
                if key.endswith(g_id):
                    subject_ids.append(key)
                    i = i + 1
                    for cell in calr[key]:
                        row.append(cell)
            #print(row)
            rows.append(row.copy())

    if get_subject_ids:
        print(subject_ids)
        sys.exit()
 
    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(subject_ids)
        #for r in final_rows:
        #    writer.writerow(r)
        writer.writerows(rows)

    sys.exit()
