import os
import sys
import xml.etree.ElementTree as ET

def extract_failures(filename):
    failures = set()
    details = {}
    root = ET.parse(filename).getroot()
    for result in root:
        for child in result:
            if child.tag.endswith('failure'):
                failures.add(child.attrib['name'])
                details[child.attrib['name']] = {
                    'class': child.attrib['class'],
                    'failure': child.text
                }

    return failures, details

def process_failures(filename_1, filename_2):

    failures_1, failures_1_details = extract_failures(filename_1)
    failures_2, failures_2_details = extract_failures(filename_2)

    # Print the symmetric difference in failures
    if failures_1 ^ failures_2:
        print ("Unique failures detected: \n")
        print ("File: %s\n" % filename_1)
        for failure in failures_1 - failures_2:
            details = failures_1_details[failure]
            print ("  %s - %s\n    %s" % (failure, details['class'], details['failure'] or ''))
        print ("\n")
        print ("File: %s\n" % filename_2)
        for failure in failures_2 - failures_1:
            details = failures_2_details[failure]
            print ("  %s - %s\n    %s" % (failure, details['class'], details['failure'] or ''))
        print ("\n")
    else:
        print("Failures are identical")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("%s file1 file2" % sys.argv[0])
        sys.exit(0)

    process_failures(sys.argv[1], sys.argv[2])
