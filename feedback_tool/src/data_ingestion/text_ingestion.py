import spacy
import os


class TextIngestion:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def preprocess_text(self, text_path):
        raw_text_data = open(os.path.join(os.path.dirname(
            __file__), text_path), "r").read()

        doc = self.nlp(raw_text_data)
        lemmatized_review = " ".join(
            [token.lemma_ for token in doc if not token.is_stop])
        return lemmatized_review
