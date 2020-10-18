import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


es = Elasticsearch("elasticsearch:9200")


def load_dataset(path):
    with open(path) as f:
        return [json.loads(line) for line in f]


def main(args):
    docs = load_dataset(args.data)
    bulk(es, docs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    args = parser.parse_args()

    main(args)
