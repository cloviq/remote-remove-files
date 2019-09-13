#!/opt/splunk/bin/python
import subprocess
import sys
import csv
import getpass
import os
from subprocess import Popen, PIPE

indexers_input = 'indexers.csv'
distribute = ''
indexers = []
copy_from = './distribute_remove_index.py'
copy_to = 'location-to-scp-to'

password = getpass.getpass(prompt="Enter password: ")

def get_inputs(indexers_input=indexers_input, distribute=distribute):
    indexers = []
    try:
        distribute_input = sys.argv[1]
        if distribute_input == 'distribute':
            distribute = 'true'
        else:
            distribute = 'false'
    except:
        distribute = 'false'

    with open(indexers_input, 'rb') as csvfile:
        indexer_file = csv.reader(csvfile)
        for row in indexer_file:
            indexers.append(row)
    indexers = indexers[0]

    return(indexers, distribute)

try:
    indexers, distribute = get_inputs()

except csv.Error as e:
    print(e)
except sys.stderr as e:
    print(e)


def scp_to_indexers(indexers=indexers, copy_from=copy_from, copy_to=copy_to):
    #os.system("scp ./distribute_remove_index.py location-scp-to")
    #PIPE =  subprocess.PIPE
    #p1 = subprocess.Popen(["echo", password, "scp", "./distribute_remove_index.py", "location-scp-to"], stdout=PIPE)
    #p2 = subprocess.Popen(password, stdin=p1.stdout, stdout=PIPE)
    #p1.communicate(input=password)
    #p1.stdout.close()
    #output = p2.communicate()
    #cmd = "echo {} | scp {} {}".format(password, copy_from, copy_to)
    try:
        cmd = ["scp", copy_from, copy_to]
        p1 = Popen(cmd, stdout=PIPE, stderr=PIPE)
        output = p1.communicate(input=password)
        p1.stdout.close()
    #print(cmd)
    #output = subprocess.check_output(cmd, shell=True)
        for item in output:
            print(item)
        print(indexers)
    except OSError as e:
        print(e)


scp_to_indexers()
