import numpy as np
from gensim.models import Word2Vec
import os

def dc_service_embedding(text: str):
    """

    :param text: str 
    :return: str
    
    This function returns 
    """
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    path_to_model = dir_path + "/Language_model/Word2Vec.model"
    model = Word2Vec.load(path_to_model)
    w2v = dict(zip(model.wv.index2word, model.wv.vectors))
    dim = len(next(iter(w2v.values())))
    embedding = np.array([
            np.mean([w2v[w] for w in text if w in w2v] or
                    [np.zeros(dim)], axis=0)])

    return embedding