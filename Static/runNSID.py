from datetime import datetime
import os.path
import os
from Static.functions import read_ripe_probe_list, read_iso_countries_list, makeatlas


def main(start, stop, ms_id):

    ts_start = str(int(datetime.timestamp(start)))
    ts_stop = str(int(datetime.timestamp(stop)))
    date = str(datetime.utcfromtimestamp(float(ts_start)).strftime('%Y%m%d'))

    beginning = 'https://atlas.ripe.net/api/v2/measurements/'
    end = '/results/?start=' + ts_start + '&stop=' + ts_stop + '&format=json'

    probefile = date + "-probemetadata.json"
    file_gz = date + '-probemetadata.json.gz'
    if os.path.exists('TempFiles/'+file_gz):
        pass

    else:
        print('ProbeMetaData did not exist')
        for item in os.listdir('TempFiles/'):
            if 'probemetadata.json.gz' in item:
                os.remove('TempFiles/'+item)

        geo_data = read_iso_countries_list()
        read_ripe_probe_list(date, probefile, geo_data)

    stats_csv_list = []
    for ns in ms_id:
        atlas_results = ns + '-' + date + "-" + ts_start + "-" + ts_stop + "-atlas-results.csv"

        if len(ns) == 3:  # if you would want both ipv4 and ipv6 in the same result file, might need some work
            m_list = [list(ns)[0] + list(ns)[1], list(ns)[0] + list(ns)[-1]]
            for m in m_list:
                measurement_id = ms_id[m]
                url = beginning + measurement_id + end
                atlas_results = makeatlas(atlas_results, url, probefile, ns)

        else:
            url = beginning + ms_id[ns] + end
            atlas_results = makeatlas(atlas_results, url, probefile, ns)

        stats_csv_list.append(atlas_results)

    nsid_rtt = []
    for file in stats_csv_list:
        with open('TempFiles/' + file, 'r') as results:
            for row in results:
                if 'ip_dst,proto,rtt,probeID,rcode' in row:
                    continue

                sp = row.split(',')
                rtt = sp[3]
                nsid = sp[8]

                if rtt != '' and nsid != '':
                    rtt = float(rtt)
                    nsid_rtt.append((nsid, rtt))

            if len(nsid_rtt) == 0:
                nsid_rtt.append((0, 0))
        results.close()

    return nsid_rtt
    # returns a list of rtt_ns lists,
    # every rtt_ns list includes rtt results from one name-server on the specified time
