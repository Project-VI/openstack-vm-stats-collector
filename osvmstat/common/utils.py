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


import libvirt
import datetime
import xml.etree.ElementTree


def domain_xml(domain):
  return xml.etree.ElementTree.fromstring(domain.XMLDesc())


def nova_metadata(domain):
  metadata = xml.etree.ElementTree.fromstring(
      domain.metadata(libvirt.VIR_DOMAIN_METADATA_ELEMENT,
      "http://openstack.org/xmlns/libvirt/nova/1.0"))
  return {"name": metadata.find("name").text,
          "project": {
          "uuid": metadata.find("owner/project").get("uuid"),
          "name": metadata.find("owner/project").text}}

