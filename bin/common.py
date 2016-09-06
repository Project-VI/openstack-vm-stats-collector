import libvirt
import xml.etree.ElementTree
import logging
import datetime


def domain_xml(domain):
    return xml.etree.ElementTree.fromstring(domain.XMLDesc())


def nova_metadata(domain):
    metadata = xml.etree.ElementTree.fromstring(
        domain.metadata(libvirt.VIR_DOMAIN_METADATA_ELEMENT,
                        "http://openstack.org/xmlns/libvirt/nova/1.0"))
    return {
        "name": metadata.find("name").text,
        "project": {
            "uuid": metadata.find("owner/project").get("uuid"),
            "name": metadata.find("owner/project").text
        }
    }


def get_logger(name):
    logger = logging.getLogger('%s' % (name))
    ch = logging.FileHandler('%s.log' % (name), mode='a')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def now():
    return datetime.datetime.now().isoformat()
