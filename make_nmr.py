#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []


def help():
    print("Description:")
    print("")
    print("This program creates an NMR file for a given Calr file and a specfied set of group IDs.")
    print("For Calr filename must end with '_CalR.csv'")
    print("The generated output filename replaces '_CalR' with '_NMR'.") 
    print("")
    print("Weights table:")
    print("Autmatically add a weights table to the generated NMR file by simply having a separate weights")
    print("table CSV file in the same directory as the ..._CalR.csv file but named with '_WEIGHTS' replacing '_CalR',")
    print("Example valid CalR filename: L25NA_L35NA_CTRL_CalR.csv")
    print("Exiample weights filename e: L25NA_L35NA_CTRL_WEIGHTS.csv")
    print("")
    print("Arguments:")
    print("* 1: A string of Group Ids, comma delimited, for example: 'L25NA,L35NA,CTRL'")
    print("* 2: The input CalR csv, for example: 'L25NA_L35NA_CTRL_CalR.csv'")
    

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
    weights = False # do not process weights by default
    weights_len = 0
    try:
        f = open(weights_f)
        weights = True
        with open(weights_f) as f:
            weights_length = len(weights_f.readlines())
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

    # get number of rows to add to rowsi[]: 
    # weights table will have a row for every target subject ID 
    # it will be added to the right of current data
    # therefore the rows to add = target subject_ids - number rows
    rows_to_add = len(target_subject_ids) - len(rows)
    # each row is idx, "NA", "NA"...
    for idx in range(rows_to_add):
        i = -1
        row = {}
        for col in rows[0].keys():
            i = i + 1
            print('idx',idx,'i',i)
            if i == 0:
                row[col] = len(rows)
                continue
            else:
                row[col] = "NA"  
        rows.append(row)
    
    # set additoinal values
    rows[1]['xrange'] = 0
    rows[2]['xrange'] = calr_length
    rows[1]['outliers'] = 'Yes'
    rows[1]['errorbars'] = 'Yes'
    rows[1]['mri'] = 'Yes'
    rows[1]['light'] = 7 
    rows[2]['light'] = 18 

    for row in rows[1:]:
        row['exc'] = calr_length
        
    

    #if weights:
        
        
    #for row in rows[1:]: # don't touch first row
    #    print('xrange',row['xrange'])
    #    for col in row.keys():
    #        #print(col) 
    #        if row[col] == '':
    #            row[col] = 'NA'

    with open(out_file, 'w') as f:
        fieldnames=rows[0]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows) 

    sys.exit()
