# Table of Contents
1. [Problem](README.md#problem)
2. [Run](README.md#run)
3. [Output Files](/output/README.md)
4. [Tests](README.md#tests)
5. [Approach](README.md#approach)
6. [Issues / TODO](README.md#issues-/-todo)


# Problem

The Office of Foreign Labor Certification (OFLC) 
[discloses data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis) on H1B (H-1B, 
H-1B1, E-3) visa application processing.  However they only provide ready-made reports for 
[2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf) 
and 
[2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf). 

This project is to provides a command line tool for identifying the occupations and states with the 
most approved H1B visas.  This allows the generation of reports using the datasets from previous 
years.


# Run

The script is run using a command such as the following:

    python3 ./src/h1b_counting.py                             \
    --input-file              ./input/h1b_input.csv           \
    --occupations-output-file ./output/top_10_occupations.txt \
    --states-output-file      ./output/top_10_states.txt
   
If you do not specify the input and output file paths.  They will default to the values above.

The script **EXPECTS CSV FILES AS INPUT** and not xlsx files.  You can convert excel files (xlsx) to
CSV with the following steps:

1.  Open the file in Microsoft Excel, Open Office, or Libra Office
2.  Clicking 'File -> Save As'
3.  Use the 'File Format' drop down menu to select 'Comma Separated Value (.csv)'.
4.  Click 'Save'

You can also convert the xlsx file to csv on the command line using a library such as [xlsx2csv](https://github.com/dilshod/xlsx2csv).

Additional usage info is available on the command line using the `--help` or `-h` option:

    usage: h1b_counting.py [-h] [-i FILE_PATH] [-o FILE_PATH] [-s FILE_PATH]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i FILE_PATH, --input-file FILE_PATH
                            File path of the CSV input file containing H1B data
      -o FILE_PATH, --occupations-output-file FILE_PATH
                            File path of the output file for writing the report on
                            Top 10 Occupations
      -s FILE_PATH, --states-output-file FILE_PATH
                            File path of the output file for writing a report on
                            Top 10 States
      -p, --profile         Enable this flag to the profile the script


# Tests

You can run the tests with the following commands:

    cd tests
    bash run_tests.sh


# Approach

The script does not load the entire file into memory so we can handle large files.  Instead it 
reads the input csv file line by line.  This is done in batches.  For each batch we create two 
lists in memory, one containing the occupation values and another containing the state values. 
Then we update the Counters using the lists.

We avoid sorting the dataset until after we aggregate on occupation and state.  We assume that both 
aggregate datesets with fit in memory at the same time.  This is reasonable because we know there's 
only 50 states and ~6500 SOC codes.



# Issues / TODO

* Not able to reproduce exact State and SOC Name counts in the ready-made reports
* Build out unit tests in tests/unit_tests.py
* Do SOC codes/names from year to year?  How to handle this.
* Read CSV file from disk in chunks to increase throughput (currently takes ~650 seconds on 10 GB file)


# Contact Us

This project was created at the request of the 
[Insight Data Engineering Fellows Program](https://insightdataengineering.com). 
