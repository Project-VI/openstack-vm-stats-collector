#! /usr/bin/python

import common
import libvirt
import json
from collections import OrderedDict # so that the timestamp is first entry

# LOG = common.get_logger('block_stats')

try:
    conn = libvirt.openReadOnly()
    if conn is None:
        raise Exception('Failed to open connection to the hypervisor')

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        block_stats = {}
        block_stats = {"devices": []}
        for dev in common.domain_xml(dom).findall("devices/disk/target"):
            devname = dev.get("dev")
            block_stats["devices"].append(devname)
            stats = dom.blockStats(devname)
            block_stats[devname] = {
                "rd_req": stats[0],
                "rd_bytes": stats[1],
                "wr_req": stats[2],
                "wr_bytes": stats[3],
                "errs": stats[4]
            }
        print json.dumps(OrderedDict([
            ("timestamp", common.now()),
            ("nova", common.nova_metadata(dom)),
            ("uuid", dom.UUIDString()),
            ("name", dom.name()),
            ("id", dom.ID()),
            ("block_stats", block_stats)
        ]))


except Exception, e:
    print json.dumps({"timestamp": common.now(), "error": "%s" % e})
