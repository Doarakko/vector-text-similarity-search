import argparse
import json
import math

import pandas as pd

from bert_server_client import BertServerClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

bsc = BertServerClient(bert_client_ip="bertserver")


def create_document(doc, vec):
    return {
        "_op_type": "index",
        "_index": args.index_name,
        "sentence": doc["sentence"],
        "sentence_vector": vec,
    }


def load_dataset(path):
    print("loading data from {}".format(path))
    df = pd.read_csv(path)
    print("total {} contents".format(len(df)))

    docs = []
    print("splitting contents")
    for row in df.iterrows():
        series = row[1]
        content = series.content
        content = bsc.preprocessing(content)
        try:
            sentences = bsc.split_sentences(content)
        except Exception:
            print("failed to split sentences: {}".format(content))
            continue

        for sentence in sentences:
            doc = {
                "sentence": sentence,
            }
            docs.append(doc)

    print("get {} sentences".format(len(docs)))
    return docs


def main(args):
    docs = load_dataset(args.data)
    n = len(docs)

    print("embedding")
    n = len(docs)
    with open(args.save, "w") as f:
        for i, doc in enumerate(docs):
            vec = bsc.sentence2vec([doc["sentence"]])
            d = create_document(doc, vec[0])
            f.write(json.dumps(d) + "\n")

            print("{} / {}".format(i + 1, n))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    parser.add_argument("--save")
    parser.add_argument("--index_name")
    args = parser.parse_args()

    main(args)
