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


import common
import json
import libvirt
import logging


def block_device_stats(dom):
  b = {}
  for d in common.domain_xml(dom).findall("devices/disk/target"):
    dev_name = d.get("dev")
    stats = dom.blockStats(dev_name)
    b.update({
        dev_name: {
            "rd_req": stats[0],
            "rd_bytes": stats[1],
            "wr_req": stats[2],
            "wr_bytes": stats[3],
            "errs": stats[4],},
        "devices": [dev_name],
    })
  return b


def main():
  logging.basicConfig(level=logging.INFO,format='%(message)s',filemode='w')

  conn = libvirt.openReadOnly()
  if conn is None:
    raise common.HypervisorConnectionFailError()

  for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    block_stats = block_device_stats(dom)
    logging.info(json.dumps({
        "nova": common.nova_metadata(dom),
        "uuid": dom.UUIDString(),
        "name": dom.name(),
        "id": dom.ID(),
        "block_stats": block_stats,}))


if __name__ == '__main__':
  main()

