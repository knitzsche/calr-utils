#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []


def help():
    print("Description:")
    print("-----------")
    print("This program creates an NMR file for a given Calr file and a specfied set of group IDs.")
    print("The CalR filename must end with '_CalR.csv'")
    print("The generated output filename is the same as the Calr file name except '_CalR' is replaced with '_NMR'.") 
    print("")
    print("Weights table:")
    print("--------------")
    print("There must be a Weights table CSV file that is named the same as the CalR file except '_CalR' is '_WEIGHTS,") 
    print("The Weights table CSV file must have data for every subject in the corresponding CalR file. Mismatches are reported.")
    print("")
    print("Arguments:")
    print("---------")
    print("* 1: A string of Group Ids, comma delimited, for example: 'L25NA,L35NA,CTRL'")
    print("* 2: The input CalR csv, for example: 'L25NA_L35NA_CTRL_CalR.csv'")
    print("")
    print("Examples:")
    print("--------")
    print("{} \"L5A,L10A,L15A,CTRL\" L5A_L10A_L15A_CTRL_CalR.csv".format(sys.argv[0]))
    print("--> Optional Weights csv file: L25NA_L35NA_CTRL_WEIGHTS.csv")
    print("'L5A_L10A_L15A_CTRL_NMR.csv' is generated.")
    print("")
    sys.exit(1) 

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()

    calr_f = sys.argv[2]
    if not calr_f.endswith('_CalR.csv'):
        print("============================================")
        print("Error: CalR filename must end with _CalR.csv'")
        print("============================================")
        help()
        sys.exit(1)  

    #calculate weights table filename from CalR filename
    weights_f = calr_f.replace('_CalR','_WEIGHTS')
    print(" ==== ", weights_f)
    weights = False # do not process weights by default
    weights_length = 0
    try:
        weights = True
        with open(weights_f) as f:
            weights_length = len(f.readlines())
    except:
        print("NOTE: No {} file found. Not adding a weight table".format(weights_f))

    out_file = calr_f.replace('_CalR','_NMR')

    calr_top_row = []
    calr_length = 0 # header and data

    # get calr_length (number of rows)
    with open(calr_f) as f:
        calr_length = len(f.readlines())

    # get header row of CalR file
    with open(calr_f) as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            i = i + 1
            if i > 0: break
            calr_top_row = row


    # get the CalR subject ID common endings, that is: the group IDs
    group_ids = sys.argv[1].split(",")
    
    calr_subject_ids = []
    groups = dict()
    # get subject IDs from the CalR calr_top_row
    for item in calr_top_row:
        subject_id = item.split("_")[-1]
        if subject_id not in calr_subject_ids:
            calr_subject_ids.append(subject_id)

    # get dict[groups] = [subject_id]
    # so that for each group, we know the subject IDs in the CalR file that match
    target_subject_ids = [] # the subject IDs in calr file that match specified group IDs
    for group_id in group_ids:
        for subject_id in calr_subject_ids:
            if subject_id.endswith(group_id):
                if group_id not in groups.keys():
                    groups[group_id] = []
                groups[group_id].append(subject_id) 
                target_subject_ids.append(subject_id)
    
    num_groups = len(groups.keys())
    rows = []
    rows.append({'':''}) # because cell 1,1 is empty in NMR csv files
    i = 0
    group_nums = [] # tracks needed group number column headers: 'group1', 'group2', etc. 
    for group_id in group_ids:
        i = i + 1
        rows[0]['group' + str(i)]='group' + str(i)
        group_nums.append('group' + str(i))
    #add additional headers (not including weights table_
    additional_headers = ['group_names','colors','xrange','outliers','errorbars','mri','light','exc'] # not weights table
    for col in additional_headers:
        rows[0][col] = col

    lengths = []
    for g in groups.keys():
        lengths.append(len(groups[g]))
    lengths.sort(reverse=True)
    longest = lengths[0] # the number of subjects in the biggest group

    for i in range(longest):
        rows.append({'':i+1})

    # populate subject IDs into 'goupX' columns
    g = 0
    for g_id in groups: # group_id
        g = g + 1
        i = 0
        for s_id in groups[g_id]: # subject_id
            i = i + 1
            rows[i]['group'+str(g)]=s_id
    
    # populate group IDs into 'group_names' column     
    g = 0
    for g_id in groups: # group_id
        g = g + 1
        rows[g]['group_names']=g_id
    
    colors = ['#FF2222','#22FF22','#2222FF','#777777','#993333','#339933','#333399','#CC2233','#339922','#2F4E7A','#8228D1','#60A260','#A12AA1']

    colors_used = [] # track colors added to nmr
    # populate colors into 'group_names' column       
    g = 0
    for g_id in groups: # group_id
        g = g + 1
        rows[g]['colors']=colors[g-1]
        colors_used.append(colors[g-1])

    # insert key/vals as needed with 'NA' as default
    for row in rows[1:]:
        for g_num in group_nums:
            if g_num not in row:
                row[g_num] = 'NA'
        for add_header in additional_headers:
            if add_header not in row:
                row[add_header] = 'NA'
    
    #additional_headers = ['group_names','colors','xrange','outliers','errorbars','mri','light','exc'] # not weights table

    # add new rows to current data (rows[]) so that the length  of rows[] is sufficent to 
    # accommodate the weights table, each row of which will be appended to 
    # data rows starting at row[1]. So if rows is is long as the number of target subject IDs
    # we'd not be able to do the appends

    # get number of rows to add to rows[]: 
    # weights table should have a row for every target subject ID 
    # it will be added to the right of current data
    # therefore the rows to add = target subject_ids - number rows
    rows_to_add = len(target_subject_ids) - len(rows) + 1
    print(target_subject_ids)
    print('len(rows)', len(rows))
    print('len(target_subject_ids)',len(target_subject_ids))
    print('rows_to_add', rows_to_add)
    #sys.exit()
    # each row is idx, "NA", "NA"...
    for idx in range(rows_to_add):
        i = -1
        row = {}
        for col in rows[0].keys():
            i = i + 1
            if i == 0:
                row[col] = len(rows)
                continue
            else:
                row[col] = "NA"  
        rows.append(row)
    
    # set additional values
    rows[1]['xrange'] = 0
    rows[2]['xrange'] = calr_length
    rows[1]['outliers'] = 'Yes'
    rows[1]['errorbars'] = 'Yes'
    rows[1]['mri'] = 'Yes'
    rows[1]['light'] = 7 
    rows[2]['light'] = 18 

    for row in rows[1:]:
        row['exc'] = calr_length
    print('weights_length',weights_length) 
    if weights:
        if weights_length < len(rows):
            print("======================================================================")
            print("ERROR: The weights table has TOO FEW ROWS.") 
            print("There should be one from row for every subject ID.")
            print("----> Your CalR file has {} subects".format(len(target_subject_ids)))
            print("----> But your WEIGHTs table has {} rows of data.".format(weights_length-1))
            print("If this is intentional, edit the the generated NMR csv file as needed.")
            print("======================================================================")
        elif weights_length > len(rows):
            print("======================================================================")
            print("ERROR: The weights table has TOO MANY ROWS.") 
            print("There should be one from row for every subject ID.")
            print("----> Your CalR file has {} subects".format(len(target_subject_ids)))
            print("----> But your WEIGHTs table has {} rows of data.".format(weights_length-1))
            print("Please fix the WEIGHTS table file and try again")
            print("======================================================================")
            sys.exit(1)

        cols = {'Total.Mass':'Total.Mass','Lean.Mass':'Lean.Mass','Fat.Mass':'Fat.Mass','id':'id'}
        rows[0].update(cols)
        with open(weights_f) as csvfile:
            reader = csv.DictReader(csvfile)
            i = 0
            for row in reader:
                i = i + 1
                rows[i].update(row)

    with open(out_file, 'w') as f:
        fieldnames=rows[0]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows) 

    sys.exit()
