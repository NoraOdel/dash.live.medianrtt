from datetime import datetime
import os.path
import os
from Static.functions import read_ripe_probe_list, read_iso_countries_list, makeatlas
from Static.fix import meta_fixer


def main(start, stop, ms_id):

    ts_start = str(int(datetime.timestamp(start)))
    ts_stop = str(int(datetime.timestamp(stop)))
    date = str(datetime.utcfromtimestamp(float(ts_start)).strftime('%Y%m%d'))

    beginning = 'https://atlas.ripe.net/api/v2/measurements/'
    end = '/results/?start=' + ts_start + '&stop=' + ts_stop + '&format=json'

    probefile = date + "-probemetadata.json"
    file_gz = date + '-probemetadata.json.gz'
    if os.path.exists('TempFiles/' + file_gz):
        pass

    else:
        meta_fixer()
        print('Probe meta data did not exist')

        geo_data = read_iso_countries_list()
        read_ripe_probe_list(date, probefile, geo_data)

    stats_csv_list = []
    for ns in ms_id:
        atlas_results = ns + '-' + date + "-" + ts_start + "-" + ts_stop + "-atlas-results.csv"

        if len(ns) == 9:  # if you would want both ipv4 and ipv6 in the same result file, might need som work
            m_list = [list(ns)[0] + list(ns)[1], list(ns)[0] + list(ns)[-1]]
            for m in m_list:
                measurement_id = ms_id[m]
                url = beginning + measurement_id + end
                atlas_results = makeatlas(atlas_results, url, probefile, ns)  # end of thing that needs work

        else:
            url = beginning + ms_id[ns] + end
            atlas_results = makeatlas(atlas_results, url, probefile, ns)

        stats_csv_list.append(atlas_results)

    rtt_list = []
    for file in stats_csv_list:
        with open('TempFiles/'+file, 'r') as results:
            rtt_ns = []
            for row in results:
                if 'ip_dst,proto,rtt,probeID,rcode' in row:
                    continue

                sp = row.split(',')
                rtt = sp[3]
                if rtt != '':
                    rtt = float(rtt)
                    rtt_ns.append(rtt)

            if len(rtt_ns) == 0:
                rtt_ns.append(0)
        results.close()
        rtt_list.append(rtt_ns)

    return rtt_list
    # returns a list of rtt_ns lists,
    # every rtt_ns list includes rtt results from one name-server on the specified time
