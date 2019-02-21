from gensim.models import doc2vec
from gensim.parsing import preprocess_string
from scraper import *

def scrape(testing = False):
    """
    Scrapes Politifact for text of all articles
    """
    stories = get_politifact_articles()
    if testing:
        stories = stories[:5]
    for url in stories:
        yield url, scrape_politifact_article(url)

class Corpus(object):
    def __init__(self, testing = False):
        self.testing = testing
        self.doc_urls = dict()
    def __iter__(self):
        for url, doc in scrape(self.testing):
            yield doc2vec.TaggedDocument(preprocess_string(doc),
                                         [url])

def build_from_corpus(documents,*args,**kwargs):
    model = doc2vec.Doc2Vec(documents,*args,**kwargs)
    return model

def preprocess_new_document(doc):
    return preprocess_string(doc)

def find_similar(doc, model, *args, **kwargs):
    cleaned_doc = preprocess_string(doc)
    inferred_vector = model.infer_vector(cleaned_doc)
    sims = model.docvecs.most_similar([inferred_vector], **kwargs)
    return sims

if __name__ == '__main__':
    # corpus = Corpus(testing=True)
    # model = build_from_corpus(corpus, vector_size=50, min_count=3, epochs=10)
    fname = "d2v_model.model"
    # model.save(fname)

    model = doc2vec.Doc2Vec.load(fname)

    new_document = "The weather in Cincinnati is very cold. Therefore global warming cannot be real."

    print(find_similar(new_document, model, topn=1))
