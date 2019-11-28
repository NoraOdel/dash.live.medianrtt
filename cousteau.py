from datetime import datetime, timedelta
from ripe.atlas.cousteau import Dns, AtlasSource, AtlasCreateRequest

msm_ids = []
time = 600
requested = 50
start = datetime.utcnow() + timedelta(minutes=10)
stop = start + timedelta(weeks=1)
adresses4 = [('192.36.144.107', 'a.ns.se'),
             ('192.36.133.107', 'b.ns.se'),
             ('192.36.135.107', 'c.ns.se'),
             ('192.71.53.53', 'f.ns.se'),
             ('130.239.5.114', 'g.ns.se'),
             ('194.146.106.22', 'i.ns.se'),
             ('199.254.63.1', 'j.ns.se'),
             ('213.108.25.4', 'x.ns.se'),
             ('185.159.197.150', 'y.ns.se'),
             ('185.159.198.150', 'z.ns.se')
             ]

ATLAS_API_KEY = ''  # from NO account
ATLAS_API_KEY_2 = ''  # from MSM account
source = AtlasSource(
    tags={'include': [], 'exclude': []},
    type='country',
    value='SE',
    requested=requested
)

for ip in adresses4:
    dns = Dns(
        target=ip[0],
        af=4,
        query_class='IN',
        query_type='SOA',
        query_argument=ip[1],
        use_macros=False,
        description='DNS measurement' + ip[0] + ' ' + ip[1],
        interval=time,
        use_probe_resolver=False,
        resolve_on_probe=False,
        set_nsid_bit=True,
        protocol='UDP',
        udp_payload_size=720,
        retry=0,
        skip_dns_check=False,
        include_qbuf=False,
        include_abuf=True,
        prepend_probe_id=False,
        set_rd_bit=False,
        set_do_bit=False,
        set_cd_bit=False,
        timeout=5000,
        type='dns'
    )

    atlas_request = AtlasCreateRequest(
        key=ATLAS_API_KEY,
        measurements=[dns],
        sources=[source],
        is_oneoff=False,
        bill_to='ulrich@wisser.se',
        start_time=start,
        stop_time=stop
    )

    (is_success, response) = atlas_request.create()
    print(response)
    print(is_success)

    measurement = (str(response['measurements'])[1:-2], ip[1] + str(4))
    msm_ids.append(measurement)

adresses6 = [('2a01:3f0:0:301::53', 'a.ns.se'),
             ('2001:67c:254c:301::53', 'b.ns.se'),
             ('2001:67c:2554:301::53', 'c.ns.se'),
             ('2a01:3f0:0:305::53', 'f.ns.se'),
             ('2001:6b0:e:3::1', 'g.ns.se'),
             ('2001:67c:1010:5::53', 'i.ns.se'),
             ('2001:500:2c::1', 'j.ns.se'),
             ('2001:67c:124c:e000::4', 'x.ns.se'),
             ('2620:10a:80aa::150', 'y.ns.se'),
             ('2620:10a:80ab::150', 'z.ns.se')
             ]

for ip6 in adresses6:
    dns = Dns(
        target=ip6[0],
        af=6,
        query_class='IN',
        query_type='SOA',
        query_argument=ip6[1],
        use_macros=False,
        description='DNS measurement' + ip6[0] + ' ' + ip6[1],
        interval=time,
        use_probe_resolver=False,
        resolve_on_probe=False,
        set_nsid_bit=True,
        protocol='UDP',
        udp_payload_size=720,
        retry=0,
        skip_dns_check=False,
        include_qbuf=False,
        include_abuf=True,
        prepend_probe_id=False,
        set_rd_bit=False,
        set_do_bit=False,
        set_cd_bit=False,
        timeout=5000,
        type='dns'
    )

    atlas_request = AtlasCreateRequest(
        key=ATLAS_API_KEY_2,
        measurements=[dns],
        sources=[source],
        is_oneoff=False,
        bill_to='ulrich@wisser.se',
        start_time=start,
        stop_time=stop
    )

    (is_success, response) = atlas_request.create()
    print(response)
    print(is_success)

    measurement = (str(response['measurements'])[1:-1], ip6[1] + str(6))
    msm_ids.append(measurement)


date = start.strftime('%Y%m%d')
ends = stop.strftime('%Y%m%d')
with open('msmIDs-' + date + '-to-' + ends, 'w') as file:
    for msm in msm_ids:
        file.write(msm[0] + ', ' + msm[1] + '\n')
file.close()
