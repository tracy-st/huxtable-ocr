## Before starting, make sure that your input list and your filenames do not include apostrophes or commas.

import os
import json
import csv
from csv import reader

##output file name
csv_file_name = ".csv"
##input file name
input_csv = ".csv"

# open file in read mode

def store_csv(csv_input):
    with open(csv_file_name, 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            csv_writer.writerow(csv_input)
        except UnicodeEncodeError:  # TODO: handle unicode OR just run with Python 3 :)
            csv_writer.writerow(["ERROR"])

def json_to_csv(input):
    with open(input_csv, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            try:

                # row variable is a list that represents a row in csv
                item = str(row[1])
                id = str(row[0])

                with open(item) as json_file:
                    all_text = ''
                    data = json.load(json_file)

                    length = len(data['responses'])

                    # for i in data['response']['docs']:
                    for i in range(length):
                            fulltext = data['responses'][i]['fullTextAnnotation']['text']
                            all_text += fulltext + ' '
                            print(id,all_text)

                    csv_response = [id, all_text]
                    store_csv(csv_response)

            except KeyError:
                    item = ""
                    id = ""
                    print("================SKIPPED==============")

json_to_csv(input_csv)