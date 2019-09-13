#!/usr/bin/python
import os
import re
import time
import shutil
import csv
import sys

index_home = '/splunk-data/'
match_pattern = r'[\w]{2}\_[\d]{10}\_[\d]{10}\_[\d]{0,4}\_[\w]{8}\-[\w]{4}\-[\w]{4}\-[\w]{4}\-[\w]{12}'
indexes_input = '/home/splunker/indexes.csv'
locations_input = 'locations.csv'

def get_inputs(indexes_input=indexes_input, locations_input=locations_input):
    ''' This function gets the inputs from the indexes_input and locations_input
        specified globally. Those files should be comma separated values for
        index names and bucket types (hot-warm, cold, frozen, thawed).
        This function also takes the parameter passed from command line for 
        whether to remove the buckets. If remove is not specified then it will
        just display the buckets it is finding.
    '''
    indexes = []
    locations = []
    try:
        remove_input = sys.argv[1]
        if remove_input == 'remove':
            remove = 'true'
        else:
            remove = 'false'
    except:
        remove = 'false'
    
    with open(indexes_input, 'rb') as csvfile:
        index_file = csv.reader(csvfile)
        for row in index_file:
            indexes.append(row)
    with open(locations_input, 'rb') as csvfile:
        location_file = csv.reader(csvfile)
        for row in location_file:
            locations.append(row)
    indexes = indexes[0]
    locations = locations[0]

    return(indexes, locations, remove)

pattern = re.compile(match_pattern)
try:
    indexes, locations, remove = get_inputs()
except:
    print('Input error.')

def remove_buckets(indexes=indexes, locations=locations, remove=remove):
    for location in locations:
        index_location = index_home + location
        for index in indexes:
            index_remove = index_location + '/' + index
            for dirname, dirnames, filenames in os.walk(index_remove):
                for dir in dirnames:
                    if re.search(pattern, dir):
                        path = os.path.join(dirname, dir)
                        if remove == 'true':
                            shutil.rmtree(path)
                            print('Removed: {}'.format(path))
                        elif remove == 'false':
                            print(path)


try:
    remove_buckets()
except:
    print('Output error.')

if remove == 'false':
    print("To remove the above buckets, call the script with 'remove' after the script name")

