#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []


def help():
    print("TODO: arg 1 is input csv, arg 2 is string of Group Ids, arg 3 is output file ")

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        if sys.argv[1] == "-h":
            help()
        if sys.argv[1] == "--help":
            help()
    #if len(sys.argv) < 4:
    #    help()
    #    sys.exit(1)
    out_file = sys.argv[3] 
    top_row = []

    with open(sys.argv[1], newline='') as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            i = i + 1
            if i > 0: break
            top_row = row

    # the CalR subject ID common endings, that is: group IDs
    group_ids = sys.argv[2].split(",")

    subject_ids = []
    groups = dict()

    # get group ids from the top row
    for item in top_row:
        subject_id = item.split("_")[-1]
        if subject_id not in subject_ids:
            subject_ids.append(subject_id)
        
    #print(subject_ids)
    for group_id in group_ids:
        for subject_id in subject_ids:
            if subject_id.endswith(group_id):
                if group_id not in groups.keys():
                    groups[group_id] = []
                groups[group_id].append(subject_id) 

    num_groups = len(groups.keys())
    rows = []
    rows.append({'':''})
    i = 0
    group_nums = [] # tracks needed group number column headers: 'group1', 'group2', etc. 
    for group_id in group_ids:
        i = i + 1
        rows[0]['group' + str(i)]='group' + str(i)
        group_nums.append('group' + str(i))
    rows[0]['group_names']='group_names'
    rows[0]['colors']='colors'

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
        for s_id in groups[g_id]: # subjet_id
            i = i + 1
            rows[i]['group'+str(g)]=s_id
    
    # populate group IDs into 'group_names' column     
    g = 0
    for g_id in groups: # group_id
        g = g + 1
        print(g,g_id)
        rows[g]['group_names']=g_id

    colors = ['#FFA6A6','#A10000','#63C3FF','#005994','#00DDAA','#DD2255','#8866AA','#CC2233','#339922','#2F4E7A','#8228D1','#60A260','#A12AA1']
    colors_used = [] # track colors added to nmr
    # populate colors into 'group_names' column       
    g = 0
    for g_id in groups: # group_id
        g = g + 1
        print(g,g_id)
        rows[g]['colors']=colors[g-1]
        colors_used.append(colors[g-1])

    # insert needed 'NA' vals since CalR does not except emtpy cells except for cell 1,1
    r = -1
    c = -1
    for row in rows:
        r = r + 1
        if r == 0: continue
        for g_num in group_nums:
            if g_num not in rows[r]:
                rows[r][g_num] = 'NA'
        if 'group_names' not in rows[r]:
            rows[r]['group_names'] = 'NA'
        if 'colors' not in rows[r]:
            rows[r]['colors'] = 'NA'
    
    with open(out_file, 'w') as f:
        fieldnames=rows[0]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerows(rows) 

    sys.exit()
