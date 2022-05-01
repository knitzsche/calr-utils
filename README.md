# Calr-Utils Introduction


Here are some python scripts that help with CalR and NMR CSV files for https://calrapp.org/.

Terms:
* Subject ID: uniquely identifies a mouse, for example: 3L25NA
* Group ID: a group of mice where the ID is the common part of the subject ID ending:
* Two mice: 3L25NA 5L25NA are both in group L25NA

The tools allow converting a default CalR file with default numeric subject IDs to be processed into new CalR files that use meaningful subject IDs/group IDs. Then you can create a new CalR file by specifiying the desired group IDs and a set of group IDs: the data for all subjects that match the group IDs are obtained from the specified CalR files and placed in a new CalR file, where the datetimes (timestamps) are pulled from the longest of the specified/input CalR files. Then, you create a correctly named Weights CSV file 9see below) and use another tool to create the NMR file for the specified CalR file.  

So, the purpose is to convert default CalR files with meaningless subject IDs into files with corrected, meaningful subject IDs, then to create from then a new (final) CalR from any set of them by specifing the groups you want. Then, automatically creating a valid NMR file by supplying only a Weiths table that contains the correct subject IDs (error are reported).

Note that the burden of ensuring data consistency is on the human being using these tools. That is, the assumption is that the timestamps of tests are equivalent among the CalR source files. 

The scripts require python 3.X (possibly 3.8) or higher. 

## Help

Each script has help that is displayed with ‘-h’ flag.

Three python scripts:
* subject_ids.py
* join.py
* make_nmr.py

# Fixing default subject IDs to meaningful IDs

subject_ids.py

Our target CalR machine generates CalR files with mouse subject IDs as simple numbers. For example: “vo2_3” where the test name is “vo2” and the subject ID is “3”. 

It is useful to have meaningful subject IDs in the CalR files because later the file can be read and understood without needing a separate map indicating which number is for which subject. 

The subect_ids.py script fixes this. It requires  a “key” file that simply maps the default subject IDs from the raw CalR file to the desired, meaningful subject IDs. 

Note: The key file is specific to a raw CalR file. You need a key file that is specific to each raw CalR file.

Example key file:
1,1L20A
2,3L20A
3,1CTRL
4,5L20A
5,4L20A
6,4CTRL
7,2L20A
8,6L20A
9,6CTRL
10,5CTRL
11,8CTRL
12,8L20A
13,3CTRL
14,7CTRL
15,2CTRL
16,7L20A

The first item in each row is the subject ID in the raw CalR file. The second item is the desired meaningful Subject ID and Group ID. 

Run the subject_ids.py script like this:

$ path/to/subject_ids.py raw_short_CalR.csv keys_short.csv fixed_short_CalR.csv 

That uses the keys_short.csv file to generate fixed_short_CalR.csv from raw_short_CalR.csv file. 

# Combining data from multiple CalR files

join.py

One may want to generate plots and analysis from calrapp for mice whose data is in more than one raw CalR file. 

Join.py takes a list of group IDs that you want and a bunch of CalR files and creates a new CalR that contains all subjects in those groups. 

The output file name is derived from the Group IDs you passed. 

For example:

$ path/to/join.py 'L5A,L10A,L15A,CTRL' two_CalR.csv short_Calr.csv three_CalR.csv

* This gets all subject data for subjects in groups L5A,L10A,L15A and CTRL
* That are in CalR files named two_CalR.csv short_Calr.csv three_CalR.csv
* And generates a file named L5A_L10A_L15A_CTRL_CalR.csv

Note: The date time values are taking from one of raw CalR files. The date time values are assumed to apply validly to all raw CalR files.

Note: Currently, the tool requires that the raw/input CalR files be listed on the command lists the longest (in lines) CalR file last.

# Generating the NMR file

make_nmr.py

This script creates an NMR file for a specified CalR file for a specified set of Group IDs. 

If there is a properly named file providing the Weights table information in the same directory, the weights table is added to the NMR file.  The Weights table file MUST be named exactly as the CalR file excepts “WEIGHTS” replaces “CalR” in the filename. 

For example:
* CalR filename: L5A_L10A_L15A_CTRL_CalR.csv
* Weights filename: L5A_L10A_L15A_CTRL_WEIGHTS.csv
* Generated NMR file: L5A_L10A_L15A_CTRL_NMR.csv

Note: If there are too few Subject IDs in the WEIGHTs file for the subject IDs contained in the CalR file, an ERROR message displays. If this is intentional, you need to edit the generated NMR file to remove the excess partial rows at the bottom of the file. 

Note: If the WEIGHTS file contains subject IDs that are not found in the CalR file, this is a logical error, and the program displays an error and stops. You must edit the WEIGHTs file to remove the extra subject IDs, or use a CalR file that contains them all. 
