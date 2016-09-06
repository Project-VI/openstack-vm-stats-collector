#! /usr/bin/python

import common
import libvirt
import json
from collections import OrderedDict # so that the timestamp is first entry

# LOG = common.get_logger("vcpus")

try:
    conn = libvirt.openReadOnly()
    if conn is None:
        raise Exception('Failed to open connection to the hypervisor')

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        vcpus = {}
        for vcpu in dom.vcpus()[0]:
            if vcpu[1] == libvirt.VIR_VCPU_OFFLINE:
                state = "offline"
            elif vcpu[1] == libvirt.VIR_VCPU_RUNNING:
                state = "running"
            elif vcpu[1] == libvirt.VIR_VCPU_BLOCKED:
                state = "blocked"
            elif vcpu[1] == libvirt.VIR_VCPU_LAST:
                state = "last"
            else:
                state = "unknown"

            vcpus[vcpu[0]] = {        # virtual CPU number
                "state": state,       # value from virVcpuState
                "cpu_time": vcpu[2],  # CPU time used, in nanoseconds
                "cpu": vcpu[3]        # real CPU number, or -1 if offline
            }

        print json.dumps(OrderedDict([
            ("timestamp", common.now()),
            ("nova", common.nova_metadata(dom)),
            ("uuid", dom.UUIDString()),
            ("name", dom.name()),
            ("id", dom.ID()),
            ("vcpus", vcpus)
        ]))

except Exception, e:
    print json.dumps({"timestamp": common.now(), "error": "%s" % e})
