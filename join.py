#!/usr/bin/python3

import csv
import sys

top1 = []
top2 = []

data1 = dict() # key is column header, val is col data list
data2 = dict() # key is column header, val is col data list


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("error. two args needs where each names a csv files")
        sys.exit(1)

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
    #for k in data2:
    #    print(data2[k])

    #sub1 = [ "10L35A","11L35A","12L35A","13L20NA","14L20NA","15L20NA","16L20NA","16L20NA","1L5A","2L5A","3L5A","4L5A","5L10A","6L10A","7L10A","8L10A","9L35A"]
    sub1 = ["L5A","L10A","L15A"]

    lines = []
    matched = []
    for k in data:
        for sub in sub1:
            if k.endswith(sub):
                matched.append(k)
                #print(k)
                #line = k+","
                for val in data[k]:
                    line += val+","        
                    print(line)
                lines.append(line)
                # remove trailing comma
                lines[len(lines)-1]=lines[len(lines-1)][:-1]
    #for line in lines:
    #    print(line)
   #     continue
  #      f = open('calr.csv', 'w')
  #      f.write(line)
  #      f.write("\n")
  #      f.flush()
  #      f.close()
        
    print(len(data.keys()))   
    #print(matched)   
