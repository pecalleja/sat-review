import argparse
import logging


parser = argparse.ArgumentParser(
    description="Read cfdis and show the resume"
)
parser.add_argument(
    "-d",
    "--directory",
    type=str,
    help="directory"
)


def main(dir_path):
    logging.info(f"Read CFDI from {dir_path}")

if __name__ == "__main__":
    FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    args = parser.parse_args()
    main(args.directory)
