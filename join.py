#!/usr/bin/python3

import csv
import sys

data = dict() # key is column header, val is col data list

def help():
    print("Description:")
    print("    This program ({}) creates a new CalR CSV file that contains the all".format(sys.argv[0]))
    print("    subject IDs that match the group IDs that you specify.")
    print("    For example if you specify a group ID of 'L5A', the all subject IDs that end with")
    print("    are obtained. You can think of it as a wildcard: *L5A. (Typically your specify multiple group IDs.) ")
    print("")
    print("    The input CalR files should already have been processed to replace numeric subject IDs, as produced")
    print("    by default by the equipment, with meanignful subject IDs. (Another tool in this tool set does this.)")
    print("")
    print("    In general, the input CalR files have column headers in this format: testname_subjectID.")
    print("        For example, three column headers: 'allmeters_14L20NA,allmeters_15L20NA,pedmeters_16L20NA,'")
    print("        * Where the tests are 'allmeters', and 'pedmeters'.") 
    print("        * Where the subject IDs are '14L20NA', '15L20NA' and '16L25A'") 
    print("        * FYI, theses subject IDs imply the following group IDs: 'L20NA', 'L25A'") 
    print("")
    print("Arguments")
    print("    1: A quoted string of comma-delimited group IDs, for example:")
    print("       'L10NA,L25NA,L35NA,CTRL'") 
    print("    2 - N:")
    print("      Any number of paths to CalR files, for example")
    print("      'a_calr.csv b_carl.csv c_calr.csv'")
    print("")
    print("Output:")
    print("    A CalR file in the current directory named based on the specified group IDs, for example:")
    print("    'L10NA_L25NA_L35NA_CTRL_NMR.csv'")    
    print("")
    print("Example:")
    print("    {} 'L10NA,L25NA,L35NA,CTRL' 'a_calr.csv b_carl.csv c_calr.csv'".format(sys.argv[0]))

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()
        sys.exit()

    get_subject_ids = False
    if "subject_ids" in sys.argv:
        get_subject_ids = True

    g_ids = sys.argv[1]
    
    # set out_file name
    out_file = ''
    for g_id in g_ids.split(','):
        out_file = out_file + g_id + '_'
    out_file = out_file[:-1] + '_CalR.csv'
    
    # read all calrs on input each into a single list of dicts
    calrs = []
    rows = []
    for f in sys.argv[2:]:
        calrs.append(f)

    # need to process sheets in from longest to shortest
    lengths_d = {} # key length, val calrs index
    lengths_l = []
    i = -1 
    for f in calrs:
        i = i + 1
        with open(f, 'r') as f:
            lengths_d[len(f.readlines())] = i
            lengths_l.append(i)
    lengths_l.sort(reverse=True)

    rows = [] # list of dicts for all input files
    sheet = -1
    for idx in lengths_l:
        f = calrs[idx]
        sheet = sheet + 1
        with open(f, newline='') as f:
            i = -1
            reader = csv.DictReader(f)
            for row in reader: # row is dict with keys being heder row cell values
                i = i + 1
                if sheet == 0:
                    rows.append(row)
                else: 
                    rows[i].update(row)

    # get all subject_ids
    all_subject_ids = [] # superset of subject IDs from input files
    for row in rows:
        for key in row.keys():
            if key not in all_subject_ids:
                all_subject_ids.append(key)

    # get the CalR subject IDs' common endings: that is, group IDs
    group_ids = g_ids.split(",")
    print('Group IDs:')
    print(group_ids)

    # get target subject_ids
    subject_ids = []
    for s_id in all_subject_ids:
        for g_id in group_ids:
            if s_id.endswith(g_id):
                if s_id in subject_ids:
                    print("Error, quitting: a subject ID has been found twice: ", s_id)
                    sys.exit(1)
                subject_ids.append(s_id) 
    print('Subgject IDs:')
    print(subject_ids)

    #remove all subject IDs that don't match group IDs
    final = []
    for row in rows:
        new_row = row.copy()
        for k in row.keys():
            if k not in subject_ids:
                del new_row[k]
        final.append(new_row)

    with open(out_file, 'w') as f:
        writer = csv.DictWriter(f, dialect='excel',fieldnames=subject_ids)
        writer.writeheader()
        for r in final:
            writer.writerow(r)

    sys.exit()
