#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []


def help():
    print("Arg 1: a RAW CalR csv file with default subject IDs.")
    print("Arg 2: a mapping file (see below)")
    print("Arg 3: the name of the FIXED CalR csv file")
    print("")
    print("The mapping file has two columns: ")
    print("    * col 1 is a default subject ID in the CalR file, typically a simple number")
    print("    * col 2 is the desired subject ID")
    print("")
    print("The program finds every subject ID in the header (the first row) ")
    print("of the RAW CalR file and changes it as specied in the mapping file,")
    print("producing a new (FIXED) CalR file as specified.")
    sys.exit(0)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()
    if len(sys.argv) < 4:
        help()
        sys.exit(1)
    in_file_calr = sys.argv[1]
    in_file_keys = sys.argv[2]
    out_file = sys.argv[3]

    keys = {}
    top_row = []
    rows = []
    # get CalR sheet
    with open(in_file_calr, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    # get keys (old subject id, new subject ID)
    with open(in_file_keys, newline='') as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            keys[row[0]] = row[1]

    new_top_row = rows[0].copy()
    i = -1
    for item in rows[0]:
        i = i + 1
        if i < 6: continue # because the first six columns of CalR file are not data
        s_id = str(item.split('_')[-1]) # gets last string after '_', the subject_id
        if s_id in keys.keys():
            base = str(item[:-len(s_id)])
            new_top_row[i] = str(base) + str(keys[s_id])
    #print(new_top_row)

    rows[0] = new_top_row.copy()

    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    sys.exit()
