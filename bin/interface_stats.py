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


def interface_macaddr_stats(dom):
  i = {}
  for d in common.domain_xml(dom).findall("devices/interface"):
    macaddr = d.find("mac").get("address")
    dev_name = d.find("target").get("dev")
    stats = dom.interfaceStats(dev_name)
    i.update({
        macaddr: {
            "rx_bytes": stats[0],
            "rx_packets": stats[1],
            "rx_errs": stats[2],
            "rx_drop": stats[3],
            "tx_bytes": stats[4],
            "tx_packets": stats[5],
            "tx_errs": stats[6],
            "tx_drop": stats[7],},
        "devices": [macaddr],
    })
  return i


def main():
  logging.basicConfig(level=logging.INFO,format='%(message)s',filemode='w')

  conn = libvirt.openReadOnly()
  if conn is None:
    raise common.HypervisorConnectionFailError()

  for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    interface_stats = interface_macaddr_stats(dom)
    logging.info(json.dumps({
        "nova": common.nova_metadata(dom),
        "uuid": dom.UUIDString(),
        "name": dom.name(),
        "id": dom.ID(),
        "interface_stats": interface_stats,}))


if __name__ == '__main__':
  main()

