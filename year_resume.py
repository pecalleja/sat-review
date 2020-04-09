import argparse
import json
import logging
import os
import xml.etree.ElementTree as etree


parser = argparse.ArgumentParser(description="Read cfdis and show the resume")
parser.add_argument("-d", "--directory", type=str, help="directory")

ns = {
    "cfdi": "http://www.sat.gob.mx/cfd/3",
    "nomina12": "http://www.sat.gob.mx/nomina12",
}


def main(dir_path):
    logging.info(f"Read CFDI from {dir_path}")
    emisor_dict = {}
    for month in range(1, 13):
        month_dir = f"{dir_path}/{month:02d}/"
        logging.info(month_dir)

        for file in os.listdir(month_dir):

            if file.endswith(".xml"):
                tree = etree.parse(f"{month_dir}{file}")
                root = tree.getroot()
                total = float(root.attrib.get("Total"))
                emisor = root.find("cfdi:Emisor", ns)
                emisor_name = emisor.attrib.get("Nombre")
                emisor_rfc = emisor.attrib.get("Rfc")
                total_cumulative = emisor_dict.get(emisor_rfc, {}).get(
                    "total", 0
                )
                month_cumulative = emisor_dict.get(emisor_rfc, {}).get(
                    f"{month:02d}", 0
                )
                if not emisor_dict.get(emisor_rfc):
                    emisor_dict[emisor_rfc] = {}

                emisor_dict[emisor_rfc].update(
                    {
                        "nombre": emisor_name,
                        "total": total + total_cumulative,
                        f"{month:02d}": total + month_cumulative,
                    }
                )
    print(json.dumps(emisor_dict, indent=4))


if __name__ == "__main__":
    FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    args = parser.parse_args()
    main(args.directory)
