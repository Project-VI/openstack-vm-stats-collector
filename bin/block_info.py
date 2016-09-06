#! /usr/bin/python

import common
import libvirt
import json
from collections import OrderedDict # so that the timestamp is first entry

# LOG = common.get_logger("block_info")

try:
    conn = libvirt.openReadOnly()
    if conn is None:
        raise Exception('Failed to open connection to the hypervisor')

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)

        block_info = {}
        block_info = {"devices": []}
        for dev in common.domain_xml(dom).findall("devices/disk/target"):
            devname = dev.get("dev")
            block_info["devices"].append(devname)
            info = dom.blockInfo(devname)
            block_info[devname] = {
                # logical size in bytes of the image
                # (how much storage the guest will see)
                "capacity": info[0],

                # host storage in bytes occupied by
                # the image (such as highest allocated
                # extent if there are no holes, similar to 'du')
                "allocation": info[1],

                # host physical size in bytes of the
                # image container (last offset, similar to 'ls')
                "physical": info[2]
            }

        print json.dumps(OrderedDict([
            ("timestamp", common.now()),
            ("nova", common.nova_metadata(dom)),
            ("uuid", dom.UUIDString()),
            ("name", dom.name()),
            ("id", dom.ID()),
            ("block_info", block_info)
        ]))

except Exception, e:
    print json.dumps({"timestamp": common.now(), "error": "%s" % e})
