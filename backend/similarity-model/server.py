from mlserver.codecs import decode_args

#Note: working on windows - does not have SigKill - i have removed the values manually, only occur twice in the files.
# Should not be a problem when working on Linux/GC later
from mlserver import MLModel
from typing import List
import numpy as np
import spacy
import os


class model(MLModel):

    async def load(self):
        self.model = spacy.load("en_core_web_lg")
    
    @decode_args
    async def predict(self, docs: List[str]) -> np.ndarray:

        doc1 = self.model(docs[0])
        doc2 = self.model(docs[1])

        return np.array(doc1.similarity(doc2))