import re
import unicodedata

from bert_serving.client import BertClient
import sentencepiece as spm
import spacy


class BertServerClient:
    def __init__(self, sp_model="model/wiki-ja.model", bert_client_ip="0.0.0.0"):
        self.sp = spm.SentencePieceProcessor()
        self.nlp = spacy.load("ja_ginza")
        self.sp.Load(sp_model)
        self.bc = BertClient(
            ip=bert_client_ip,
            output_fmt="list",
        )

    def split_sentences(self, text):
        doc = self.nlp(text)
        return [s.text for s in doc.sents]

    def __clean_text(self, text):
        replaced_text = re.sub(r"[【】]", " ", text)
        replaced_text = re.sub(r"[\[\]]", " ", replaced_text)
        replaced_text = re.sub(r"[・]", "", replaced_text)
        replaced_text = re.sub(r"[\"“”]", " ", replaced_text)
        replaced_text = re.sub(r"[■▼▶●]", " ", replaced_text)
        replaced_text = re.sub(r"[「」]", " ", replaced_text)
        replaced_text = re.sub(r"[※]", " ", replaced_text)
        # delete the tags and parentheses together with the contents
        replaced_text = re.sub(r"(\(.*\))", "", replaced_text)
        replaced_text = re.sub(r"(<.*>)", "", replaced_text)
        # delete the thread number like ">>14"
        replaced_text = re.sub(r"(>{2}\d+)", "", replaced_text)
        return replaced_text

    def __clean_url(self, html_text):
        return re.sub(r"http\S+", "", html_text)

    def __normalize_unicode(self, text, form="NFKC"):
        return unicodedata.normalize(form, text)

    def __normalize_number(self, text):
        return re.sub(r"\d+", "0", text)

    def __lower_text(self, text):
        return text.lower()

    def preprocessing(self, text):
        text = self.__clean_url(text)
        text = self.__normalize_unicode(text)
        text = self.__lower_text(text)
        text = self.__clean_text(text)
        text = self.__normalize_number(text)
        return text

    def __sentence_piece_tokenizer(self, text):
        return self.sp.EncodeAsPieces(text)

    def sentence2vec(self, sentences):
        parsed_texts = list(map(self.__sentence_piece_tokenizer, sentences))
        return self.bc.encode(parsed_texts, is_tokenized=True)
