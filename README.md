# Vector text similarity search

Search for similar documents using Elasticsearch and BERT.  
This assumes Japanese sentences.

## Requirement

- docker-compose

## Usage

```
$ docker-compose up --build
```

### Init

1. Download and set up the model file

Download from [here](https://drive.google.com/drive/folders/1Zsm9DD40lrUVu6iAnIuTH2ODIkh-WM-O).

Rename download files like this.

```
$ ls bertserver/model
bert_config.json			bert_model.ckpt.meta			wiki-ja.model
bert_model.ckpt.data-00000-of-00001	graph.pbtxt				wiki-ja.vocab
bert_model.ckpt.index			vocab.txt
```

2. Go to JupyterLab(`http://0.0.0.0:8888/lab`) and open terminal

3.  Create Elasticsearch index

```
$ python create_index.py --index_file index.json --index_name vector_search
```

3. Create Elasticsearch documents

```
$ python create_documents.py --data contents.csv --save contents.json --index_name vector_search
```

4. Index Elasticsearch documents

```
$ python index_document.py --data contents.json
```

5. Open `main.ipynb` and run


## Hints

### Expected data format

csv and japanese are expected.

| content                                                                  |
| :----------------------------------------------------------------------- |
| 私は仕事中によく居眠りをしてしまいます。眠気を覚ます方法を教えて下さい。 |

`content` can be multiple sentences.  
It is split into one sentence during preprocessing

## Reference

- [ベクトルフィールドを使ったテキスト類似性検索](https://www.elastic.co/jp/blog/text-similarity-search-with-vectors-in-elasticsearch)
- [Elasticsearch と BERT を組み合わせて類似文書検索](https://hironsan.hatenablog.com/entry/elasticsearch-meets-bert)
- [BERT with SentencePiece を日本語 Wikipedia で学習してモデルを公開しました](https://yoheikikuta.github.io/bert-japanese/)
- [ElasticsearchでSudachiとベクトル検索を組み合わせて使う方法 ①Sudachi導入編](https://www.ai-shift.co.jp/techblog/168)
- [ElasticsearchでSudachiとベクトル検索を組み合わせて使う方法 ②ベクトル検索編](https://www.ai-shift.co.jp/techblog/460)
- [検索エンジンにBERTを組み合わせて検索性能を向上させる手法](https://hironsan.hatenablog.com/entry/faq-retrieval-using-query-question-similarity-and-bert-based-query-answer-relevance)
