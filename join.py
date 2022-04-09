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

    calrs = []
    rows = [] # list of dicts for all input files
              # keys are header row if each input file
    # read all calrs on input each into a single list of dicts
    if ',' in in_fs:
        calrs = in_fs.split(',')
    else:
        calrs = [in_fs]
    sheet = -1
    for f in calrs:
        sheet = sheet + 1
        with open(f, newline='') as f:
            i = -1
            reader = csv.DictReader(f)
            # TODO: fix this. the new source sheet is added as new row but needs to be appended to equiv row
            for row in reader: # row is dict with keys being heder row cell values
                i = i + 1
                if sheet == 0:
                    rows.append(row)
                else: 
                    if i == 0: 
                        print('================================')
                        print("before",len(rows[i]))
                    rows[i].update(row)
                    if i == 0: 
                        print("after",len(rows[i]))

    # get all subject_ids
    all_subject_ids = [] # superset of subject IDs from input files
    for row in rows:
        for key in row.keys():
            if key not in all_subject_ids:
                all_subject_ids.append(key)
    #print(all_subject_ids)

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
