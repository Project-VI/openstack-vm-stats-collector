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


def block_device_info(dom):
  b = {}
  for d in utils.domain_xml(dom).findall("devices/disk/target"):
    dev_name = d.get("dev")
    info = dom.blockInfo(dev_name)
    b.update({
        dev_name: {
            "capacity": info[0],
            "allocation": info[1],
            "physical": info[2],},
        "devices": [dev_name],
    })
  return b


def main():
  conn = libvirt.openReadOnly()
  if conn is None:
    raise exceptions.HypervisorConnectionFailError()

  for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    block_info = block_device_info(dom)
    print(json.dumps({
        "nova": utils.nova_metadata(dom),
        "uuid": dom.UUIDString(),
        "name": dom.name(),
        "id": dom.ID(),
        "block_info": block_info,}))


if __name__ == '__main__':
  main()

