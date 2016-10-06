#!/usr/bin/env python
# coding=utf-8
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import libvirt


from common import utils
from common import exceptions


def vcpu_state(state_code):
    if state_code == libvirt.VIR_VCPU_OFFLINE:
        state = "offline"
    elif state_code == libvirt.VIR_VCPU_RUNNING:
        state = "running"
    elif state_code == libvirt.VIR_VCPU_BLOCKED:
        state = "blocked"
    elif state_code == libvirt.VIR_VCPU_LAST:
        state = "last"
    else:
        state = "unknown"
    return state


def cpu_used_info(dom):
    d = {}
    for t in dom.vcpus()[0]:
        d.update({
            t[0]: {
                "state": vcpu_state(t[1]),
                "cpu_time": t[2],
                "cpu": t[3],
                }})
    return d


def main():
    conn = libvirt.openReadOnly()
    if conn is None:
        raise exceptions.HypervisorConnectionFailError()

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        vcpus = cpu_used_info(dom)
        print(json.dumps({
            "nova": utils.nova_metadata(dom),
            "uuid": dom.UUIDString(),
            "name": dom.name(),
            "id": dom.ID(),
            "vcpus": vcpus,
            }))


if __name__ == '__main__':
    main()
