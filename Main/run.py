import sys
from datetime import datetime, timedelta
import os.path
import os
sys.path.append('../')
from Main.functions import read_ripe_probe_list, read_iso_countries_list, makeatlas


def main():
    nameserver = ['a4', 'b4']
    statsCSV_list = []
    ms_id = {
        'a4': '23033112',
        'b4': '23033001'}

    start = datetime.utcnow()
    stop = start + timedelta(minutes=10)

    ts_start = str(int(datetime.timestamp(start)))
    ts_stop = str(int(datetime.timestamp(stop)))
    date = str(datetime.utcfromtimestamp(float(ts_start)).strftime('%Y%m%d'))

    beginning = 'https://atlas.ripe.net/api/v2/measurements/'
    end = '/results/?start=' + ts_start + '&stop=' + ts_stop + '&format=json'


    probeFile = date + "-probemetadata.json"
    file_gz = date + '-probemetadata.json.gz'
    if os.path.exists(file_gz):
        pass

    else:
        print('ProbeMetaData did not exist')

        for item in os.listdir():
            if 'probemetadata.json.gz' in item:
                os.remove(item)

        geo_data = read_iso_countries_list()
        read_ripe_probe_list(date, probeFile, geo_data)

    for ns in nameserver:
        atlas_results = ns + '-' + date + "-" + ts_start + "-" + ts_stop + "-atlas-results.csv"

        if len(ns) == 3:
            m_list = [list(ns)[0] + list(ns)[1], list(ns)[0] + list(ns)[-1]]

            for m in m_list:
                measurementID = ms_id[m]
                url = beginning + measurementID + end
                atlas_results = makeatlas(atlas_results, url, probeFile, ns)

        else:
            measurementID = ms_id[ns]
            url = beginning + measurementID + end
            atlas_results = makeatlas(atlas_results, url, probeFile, ns)

        statsCSV_list.append(atlas_results)
    print('\nIf WARNING occurred some measurements were empty. Do not panic!!!'.upper())

    list_mean_rtt = []
    for file in statsCSV_list:
        with open(file, 'r') as results:
            rtt_list = []
            for row in results:
                if 'ip_dst,proto,rtt,probeID,rcode' in row:
                    continue

                sp = row.split(',')
                rtt = sp[3]
                if rtt != '':
                    rtt = float(rtt)
                    rtt_list.append(rtt)

            if len(rtt_list) == 0:
                rtt_list.append(0)

        list_mean_rtt.append(sum(rtt_list)/len(rtt_list))

    return list_mean_rtt







