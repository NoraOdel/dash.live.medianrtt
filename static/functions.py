from ripe.atlas.sagan import DnsResult
import bz2
import json
import requests
import gzip
import os
import csv
import dns.message
import base64
from datetime import datetime, timedelta


def json_parser(f):
    answers = []
    try:
        measurement = json.loads(f)
    except:
        print("Error loading json")

    for lines in measurement:
        try:
            my_results = DnsResult(lines)
            src_result = my_results.responses[0].source_address
            dst_result = my_results.responses[0].destination_address
            proto_result = my_results.responses[0].protocol
            rtt_result = my_results.responses[0].response_time
            abuf = str(my_results.responses[0].abuf)
            dnsmsg = dns.message.from_wire(base64.b64decode(abuf))
            rcode = dnsmsg.rcode()
            prb_id = lines['prb_id']
            fw = lines['fw']
            timestamp = lines['timestamp']

            answers.append(str(src_result) + ',' + str(dst_result) + ',' + str(proto_result) + ',' +
                           str(rtt_result) + ',' + str(prb_id) + ',' + str(rcode) + ',' +
                           str(fw) + ',' + str(timestamp))

        except:
            print('EMPTY measurement \n')
            answers.append(',' + ',' + ',' + ',' + ',' + ',' + ',')

    return answers


def read_probe_data(f, measurementID):

    f = gzip.open(f, 'rb')
    metadata = f.read()
    metadata = metadata.decode("utf-8")
    f.close()

    appendDict = dict()
    items = json.loads(metadata)

    for k in items['objects']:
        prid = k['id']

        trailler = k['country_code']+","+k['continent']+","+k['sub_region']+","+str(k['longitude'])+','+str(k['latitude'])+','+str(measurementID)
        appendDict[str(prid)] = trailler

    return appendDict


def read_iso_countries_list():

    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
    r = requests.get(url)
    print("Download regions code list from :\n" + url)
    cr = csv.reader(r.content.decode("utf-8").split("\n"))
    countryCode_info = dict()

    for row in cr:
        if len(row) > 2:
            countryCode_info[row[1]] = row

    return countryCode_info


def read_ripe_probe_list(date, probeFile, geo_data):

    url = "https://ftp.ripe.net/ripe/atlas/probes/archive"
    date_before = datetime.strftime(datetime.strptime(date, '%Y%m%d') - timedelta(days=1), '%Y%m%d')

    datebefore = date_before[0:4]+date_before[4:6]+date_before[6:8]
    url = url+"/"+date_before[0:4]+"/"+date_before[4:6]+"/" + datebefore+".json.bz2"

    print('Downloading ripe database from: \n' + url, '\n')
    r = requests.get(url)
    decompressed = (bz2.decompress(r.content)).decode("utf-8")

    j = json.loads(decompressed)
    outz = open(probeFile, 'w')

    tempList = j['objects']
    newDict = j
    newDict['objects'] = []

    newList = []
    for item in tempList:
        tempCC = item['country_code']

        if type(tempCC) is not None and tempCC != "" and str(tempCC) != "None":
            tempStr = geo_data[tempCC]

            continent = tempStr[5]
            sub_region = tempStr[6]
            intermediate_region = tempStr[7]

            item['continent'] = continent
            item['sub_region'] = sub_region
            item['intermediate_region'] = intermediate_region

            newList.append(item)
    newDict['objects'] = newList

    json.dump(newDict, outz)
    outz.close()

    with open(probeFile, 'rb') as f_in, gzip.open(probeFile+'.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    os.remove(probeFile)


def makeatlas(atlas_results, url, probeFile, ns):
    r = requests.get(url)
    measurements = json_parser(r.content.decode("utf-8"))
    probeDict = read_probe_data(probeFile + ".gz", ns)

    with open(atlas_results, 'a') as csvFileFromAtlas:
        csvFileFromAtlas.write(
            "ip_src,ip_dst,proto,rtt,probeID,rcode,atlas_firmware,timestamp,"
            "country,continent,subregion,longitud,latitud,measurementID\n")

        probes_not_found = 0
        for k in measurements:
            probeID = k.split(",")[4]
            trailler = "NA,NA"

            try:
                trailler = probeDict[probeID.strip()]
            except:
                # if trailler is empty the measurement had no data and the probe can't be found
                probes_not_found += 1
            csvFileFromAtlas.write(k + "," + trailler + "\n")
    csvFileFromAtlas.close()
    return atlas_results