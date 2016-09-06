#! /usr/bin/python

import common
import libvirt
import json
from collections import OrderedDict # so that the timestamp is first entry

# LOG = common.get_logger("memory_stats")

try:
    conn = libvirt.openReadOnly()
    if conn is None:
        raise Exception('Failed to open connection to the hypervisor')

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        print json.dumps(OrderedDict([
            ("timestamp", common.now()),
            ("nova", common.nova_metadata(dom)),
            ("uuid", dom.UUIDString()),
            ("name", dom.name()),
            ("id", dom.ID()),
            ("memory_stats", dom.memoryStats())
        ]))

except Exception, e:
    print json.dumps({"timestamp": common.now(), "error": "%s" % e})
