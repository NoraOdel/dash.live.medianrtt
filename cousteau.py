from datetime import datetime, timedelta
from ripe.atlas.cousteau import Dns, AtlasSource, AtlasCreateRequest

msm_ids = []
time = 'VET EJ ÄN'
requested = 'VET EJ ÄN'
start = datetime.utcnow()
stop = start + timedelta(weeks=1)
adresses = [('192.36.144.107', 'a.ns.se'),
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

ATLAS_API_KEY = 'OPS'
source = AtlasSource(
    tags={'include': [], 'exclude': []},
    type='country',
    value='SE',
    requested=requested
)

for ip in adresses:
    dns = Dns(
        target=ip[0],
        af=4,
        query_class='IN',
        query_type='SOA',
        query_argument=ip[0],
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
        start_time=start,
        stop_time=stop
    )

    (is_success, response) = atlas_request.create()

    msm_ids.append((response['measurements'], ip[1]))
    print(response)
    print(is_success)


with open('measurementIDs', 'w') as file:
    for msm in msm_ids:
        file.write(msm[0] + ', ' + msm[1] + '\n')
file.close()
