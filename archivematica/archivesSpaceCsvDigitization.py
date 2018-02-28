#!/usr/bin/env python

import os, csv

# This has two columns, and no header row.  First column has file name, 2nd has ref id from ASpace

def makeRow(filename,refid):
    row = []
    row.append(filename)
    row.append(refid)
    writer.writerow(row)

# input refid
refid = raw_input('Enter the ArchivesSpace refid: ')

access_directory = 'archivematica_sip_' + refid + '/objects/access/'

metadata_directory = 'archivematica_sip_' + refid + '/metadata/'

filenames = os.listdir(access_directory)
print filenames

print 'Creating a csv'
os.chdir(metadata_directory)
spreadsheet = 'archivesspaceids.csv'
writer = csv.writer(open(spreadsheet, 'w'))
for filename in filenames:
    makeRow(filename,refid)
print 'Done!'