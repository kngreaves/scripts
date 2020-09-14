#!/usr/bin/env python

import base64
import json
import os
import requests
import time
from shutil import rmtree

# directory of transfers; needs to be an Archivematica transfer source
queue_directory = '/path/to/directory'
transfers = os.listdir(queue_directory)
transfers = [e for e in transfers if e not in ('.DS_Store', 'Thumbs.db')]
print("----------- {} directories left to ingest -----------".format(str(len(transfers))))


username = 'user'  # dashboard username
apikey = 'apikey'  # api key for dashboard user
headers = {"Authorization": "ApiKey {}:{}".format(username, apikey)}
baseurl = 'http://dashboard-ip/api'
location_uuid = 'location-uuid'  # UUID for transfer source

output_file = "/path/to/file/filename.txt"


def hide_packages(tab):
    # tab must be "ingest" or "transfer"
    completed_list = requests.get(
        os.path.join(
            baseurl,
            tab,
            'completed'),
        headers=headers).json().get('results')
    print("Removing {} completed {}s from the dashboard".format(str(len(completed_list)), tab))
    for c in completed_list:
        requests.delete(
            os.path.join(
                baseurl,
                tab,
                c,
                'delete'),
            headers=headers)


def document_result(output_file, result, rfod):
    current_time = time.strftime(" %b %d %H:%M")
    s = "\n{} - {} - {}".format(rfod, result, current_time)
    with open(output_file, 'a') as f:
        f.write(s)


# remove completed transfers and ingests from the dashboard before
# starting ingest loop
hide_packages('transfer')
hide_packages('ingest')

count = 0


while True:
    for txfr in transfers:
        if int(time.strftime("%H")) >= 20:
            break
        else:
            # count += 1
            document_result(output_file, "started", txfr[4:])
            print("Starting " + txfr[4:] + " - " +
                  time.strftime(" %b %d %H:%M:%S"))
            basepath = os.path.join(queue_directory, txfr)
            full_url = os.path.join(baseurl, 'transfer/start_transfer/')
            bagpaths = "{}:{}".format(location_uuid, basepath)
            params = {'name': txfr[4:], 'type': 'standard',
                      'paths[]': base64.b64encode(bagpaths.encode())}
            start = requests.post(full_url, headers=headers, data=params)
            print(start.json()['message'] + time.strftime(" %b %d %H:%M:%S"))
            time.sleep(10)
            loopNumber = 0
            while True:
                unapproved_transfers = requests.get(
                    os.path.join(
                        baseurl,
                        'transfer/unapproved'),
                    headers=headers).json().get('results')
                if unapproved_transfers:
                    transferUuid = unapproved_transfers[0].get('uuid')
                    break
                elif loopNumber >= 10:
                    break
                else:
                    print("No transfers awaiting approval")
                    loopNumber += 1
                    time.sleep(5)
            approve_transfer = requests.post(os.path.join(baseurl,
                                                          'transfer/approve_transfer/'),
                                             headers=headers,
                                             data={'type': 'standard',
                                                   'directory': txfr[4:]})
            print(
                approve_transfer.json()['message'] +
                time.strftime(" %b %d %H:%M:%S"))
            # print(transferUuid)
            transferStatusUrl = os.path.join(
                baseurl, 'transfer/status/', transferUuid)
            time.sleep(400)
            while True:
                transferStatus = requests.get(
                    transferStatusUrl, headers=headers).json().get('status')
                if transferStatus == 'COMPLETE':
                    time.sleep(30)
                    sipUuid = requests.get(
                        transferStatusUrl, headers=headers).json().get('sip_uuid')
                    ingestStatusUrl = os.path.join(
                        baseurl, 'ingest/status/', sipUuid)
                    time.sleep(600)
                    rmtree(os.path.join(queue_directory, txfr))
                    while True:
                        ingestStatus = requests.get(
                            ingestStatusUrl, headers=headers).json().get('status')
                        if ingestStatus == 'COMPLETE':
                            document_result(
                                output_file, "ingest completed", txfr[4:])
                            break
                        elif ingestStatus == 'FAILED':
                            document_result(
                                output_file, "ingest failed", txfr[4:])
                            break
                        time.sleep(15)
                    break
                elif transferStatus == 'FAILED':
                    break
                time.sleep(5)
            print(txfr[4:] + " complete -" + time.strftime(" %b %d %H:%M:%S"))
    break
