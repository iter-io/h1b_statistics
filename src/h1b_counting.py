
from argparse import ArgumentParser
from collections import Counter
from csv import DictReader, DictWriter, Sniffer
from itertools import chain, filterfalse, islice
from os import path
from time import perf_counter


def main():
    """
    Main function that does the counting.  For each batch of applications we create two lists in
    memory, one containing the occupation values and another containing the state values.  Then we
    use these lists to update the counter.

    :return:
    """
    # Parse the command line args
    args = get_args()

    state_counter = Counter()
    occupation_counter = Counter()

    # Process the application data in batches
    for batch in certified_application_batches(args.input_file, 100000):
        # Create lists of values for each batch
        states = []
        occupations = []
        for row in batch:
            states.append(row['WORKSITE_STATE'])
            occupations.append(row['SOC_NAME'])

        state_counter.update(states)
        occupation_counter.update(occupations)

    # Write our output files
    write_top10_file(args.states_output_file, state_counter, 'TOP_STATES')
    write_top10_file(args.occupations_output_file, occupation_counter, 'TOP_OCCUPATIONS')


def write_top10_file(output_file, counter, dimension_name):
    """
    Writes a csv file containing the 10 most frequent values from a counter. Each line of the
    output file will contain these fields in this order:
    
    DIMENSION_NAME:                 Value of the dimension associated the row.

    NUMBER_CERTIFIED_APPLICATIONS:  Number of applications that have been certified for the
                                    dimension value associated with the row.

    PERCENTAGE:                     % of total applications certified for the dimension value
                                    associated with the row.
    

    The records are sorted by NUMBER_CERTIFIED_APPLICATIONS, and in case of a tie, alphabetically
    by the value of the dimension_name parameter.

    We can't use Counter.most_common(10) because elements with equal counts are ordered
    arbitrarily (see test 3).  The problem arises when there is a tie for 10th place.

    :param output_file:
    :param counter:
    :param dimension_name:
    :return:
    """
    print('Writing output file: {0}'.format(output_file))

    # Create a sorted list of tuples using a compound key consisting of count and dimension value
    top10 = sorted(counter.most_common(), key=lambda x: (-x[1], x[0]))[:10]

    # Get the total number of certified applications
    total = sum(counter.values())

    # Write the file
    with open(output_file, 'w') as csv_file:
        fieldnames = [dimension_name, 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
        writer = DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()

        for row in top10:
            dimension, count = row
            writer.writerow({
                dimension_name: dimension,
                'NUMBER_CERTIFIED_APPLICATIONS': count,
                'PERCENTAGE': str(round((count / total) * 100, 1)) + '%'
            })


def certified_application_batches(csv_file_path, batch_size):
    """
    Returns an iterator for each batch for certified applications.

    :param csv_file_path:
    :param batch_size:
    :return:
    """
    source_iter = read_certified_applications(csv_file_path)
    while True:
        batch_iter = islice(source_iter, batch_size)

        # https://www.python.org/dev/peps/pep-0479/
        try:
            yield chain([next(batch_iter)], batch_iter)
        except StopIteration:
            return



def read_certified_applications(csv_file_path):
    """
    Generator function for reading the input CSV files.  This function does the following:

    1.  We sniff the file format so we can support both default excel formatted csv and the
        semi-colon separated files (see Test 1 and Test 2).

    2.  We check if the file uses the previous LCA record layout. If so, we migrate it to the
        current H1B Record Layout.

    3.  Filter out all application that are not 'CERTIFIED'.

    The goal of this function is to separate code for reading the input file format from our
    analytical code.

    :param csv_file_path:
    :return:
    """
    print('Processing input file: {0}'.format(csv_file_path))

    with open(csv_file_path) as csv_file:

        # Sniff the file format
        dialect = Sniffer().sniff(csv_file.read(16384))
        csv_file.seek(0)

        reader = DictReader(csv_file, dialect=dialect)

        # Dirty migration of the previous LCA Record Layout to the current H1B Record Layout
        if 'LCA_CASE_NUMBER' in reader.fieldnames:
            reader.fieldnames = get_migrated_fieldnames()

        # Filter all applications that are not certified
        yield from filterfalse(lambda row: row['CASE_STATUS'] != 'CERTIFIED', reader)


def get_migrated_fieldnames():
    """
    This is used to crudely migrate the field names in the previous LCA Record
    Layout to the new field names in the current H1B Record Layout.

    :return:
    """
    return [
        "",
        "CASE_NO",
        "CASE_STATUS",
        "CASE_SUBMITTED",
        "DECISION_DATE",
        "VISA_CLASS",
        "EMPLOYMENT_START_DATE",
        "EMPLOYMENT_END_DATE",
        "EMPLOYER_NAME",
        "EMPLOYER_ADDRESS1",
        "EMPLOYER_CITY",
        "EMPLOYER_STATE",
        "EMPLOYER_POSTAL_CODE",
        "SOC_CODE",
        "SOC_NAME",
        "JOB_TITLE",
        "WAGE_RATE_OF_PAY",
        "WAGE_RATE_TO",
        "WAGE_UNIT_OF_PAY",
        "FULL_TIME_POSITION",
        "TOTAL WORKERS",
        "WORKSITE_CITY",
        "WORKSITE_STATE",
        "PREVAILING_WAGE",
        "PW_UNIT_OF_PAY",
        "PW_WAGE_SOURCE",
        "PW_WAGE_SOURCE_OTHER",
        "PW_WAGE_SOURCE_YEAR",
        "WORKSITE_CITY_2",
        "WORKSITE_STATE_2",
        "PREVAILING_WAGE_2",
        "PW_UNIT_OF_PAY_2",
        "PW_WAGE_SOURCE_2",
        "PW_WAGE_SOURCE_OTHER_2",
        "PW_WAGE_SOURCE_YEAR_2",
        "NAIC_CODE"
    ]


def get_args():
    """
    We use named command line args to make the script a little more user-friendly. This function
    parses them for us. We also check if the output file paths exist before we do all the heavy
    work.

    :return:
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-i", "--input-file",
        action="store",
        dest="input_file",
        default="./input/h1b_input.csv",
        help="File path of the CSV input file containing H1B data",
        metavar="FILE_PATH"
    )

    parser.add_argument(
        "-o", "--occupations-output-file",
        action="store",
        dest="occupations_output_file",
        default="./output/top_10_occupations.txt",
        help="File path of the output file for writing the report on Top 10 Occupations",
        metavar="FILE_PATH"
    )

    parser.add_argument(
        "-s", "--states-output-file",
        action="store", dest="states_output_file", default="./output/top_10_states.txt",
        help="File path of the output file for writing a report on Top 10 States",
        metavar="FILE_PATH"
    )

    args = parser.parse_args()

    # Check if the file paths from the user are valid
    for file_path in [args.input_file, args.occupations_output_file, args.states_output_file]:
        if not path.isdir(path.dirname(file_path)):
            print("error: invalid file path:  " + file_path)
            exit(1)

    return args


if __name__ == "__main__":
    start = perf_counter()
    main()
    stop = perf_counter()
    print('Runtime: {0}s'.format(round(stop - start, 2)))

