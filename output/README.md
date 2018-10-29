# Output Files

By default the output of h1b_counting.py goes to this directory (./output).  You can override this 
behavior using the `--occupations-output-file` and `--states-output-file` command line options.  For 
example:

    python3 ./src/h1b_counting.py \
        --occupations-output-file ./output/my_occupations_output_file.txt \
        --states-output-file ./output/my_states_output_file.txt

For more info use --help:

    python3 ./src/h1b_counting.py --help


# Output File Format

h1b_counting.py creates 2 output files:

1.  A file containing the Top 10 occupations for certified visa applications.  This output file is
    specified using the `--occupations-output-file` command line option (defaults to 
    ./output/top_10_occupations.txt).
    
    Each line holds one record and each field on each line is separated by a semicolon (;).
    
    Each line of the top_10_occupations.txt file should contain these fields in this order:
    
    TOP_OCCUPATIONS: Use the occupation name associated with an application's Standard Occupational Classification (SOC) code
    NUMBER_CERTIFIED_APPLICATIONS: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of Certified
    PERCENTAGE: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation.
    The records in the file must be sorted by NUMBER_CERTIFIED_APPLICATIONS, and in case of a tie, alphabetically by TOP_OCCUPATIONS.

 
2.  A file containing the Top 10 states for certified visa applications

    Each line of the top_10_states.txt file should contain these fields in this order:
    
    TOP_STATES: State where the work will take place
    NUMBER_CERTIFIED_APPLICATIONS: Number of applications that have been certified for work in that state. An application is considered certified if it has a case status of Certified
    PERCENTAGE: % of applications that have been certified in that state compared to total number of certified applications regardless of state.
    The records in this file must be sorted by NUMBER_CERTIFIED_APPLICATIONS field, and in case of a tie, alphabetically by TOP_STATES.
    
    Depending on the input (e.g., see the example below), there may be fewer than 10 lines in each file. There, however, should not be more than 10 lines in each file. In case of ties, only list the top 10 based on the sorting instructions given above.
    
    Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and 1.04% should be rounded to 1.0%. Also, 1% should be represented by 1.0%