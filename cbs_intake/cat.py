import requests
import xml.etree.ElementTree as ET
import yaml
import tempfile
import os
import logging


CACHE_FILE = "cbs_intake_catalog_cache"
TABLES_URL = "https://opendata.cbs.nl/ODataCatalog/Tables"


def download_data():
    '''downloads data if doesn't exist, otherwise use cachefile version'''

    dr = tempfile.gettempdir()
    fn = os.path.join(dr, CACHE_FILE)
    if os.path.exists(fn):
        logging.debug(f"Reading file from cachefile {fn}.")
        text = open(fn).read()
    else:
        response = requests.get(TABLES_URL)
        text = response.text
        with open(fn, "w") as f:
            f.write(text)

    return text


def list_entries(text):
    '''parse text into catalog entries'''

    root = ET.fromstring(text)

    # strip namespaces
    for el in root.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

    entries = list()
    for entry in root.findall("entry"):
        try:
            entries.append(entry_to_source(entry))
        except KeyError as e:
            logging.info(f"Failed to parse {entry} because of {e}.")
    return entries


def entry_to_source(entry):

    d = cbs_xml_to_dict(entry)
    props = d["content"]["properties"]
    
    return props["Identifier"], {
        "description": props["ShortDescription"],
        "driver": 'cbs-odata',
        "metadata": d,
        "args": {
            "url": props["ApiUrl"]
        }
    }


def write_to_file(fn):

    text = download_data()
    entries = list_entries(text)

    d = {
        "metadata": {
            "version": 1
        },
        "sources": {
            name: entry for name, entry in entries
        }
    }

    with open(fn, "w") as f:
        yaml.dump(d, f)


def cbs_xml_to_dict(el):

    if el.text:
        return el.text

    return {
        child.tag: cbs_xml_to_dict(child) for child in el.getchildren()
    }
