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
import logging


from common import utils
from common import exceptions


def main():
  logging.basicConfig(level=logging.INFO,format='%(message)s',filemode='w')

  conn = libvirt.openReadOnly()
  if conn is None:
    raise exceptions.HypervisorConnectionFailError()

  for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    logging.info(json.dumps({
        "nova": utils.nova_metadata(dom),
        "uuid": dom.UUIDString(),
        "name": dom.name(),
        "id": dom.ID(),
        "memory_stats": dom.memoryStats(),}))


if __name__ == '__main__':
  main()

