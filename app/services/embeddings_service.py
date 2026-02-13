import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize a local embedding model. Change the model name if you prefer
# a different sentence-transformers model. This loads at import time.
_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_embedder = SentenceTransformer(_EMBED_MODEL_NAME)


def get_embedding(text: str):
    try:
        vec = _embedder.encode(text)
        return np.array(vec)
    except Exception as e:
        print(f"Embedding failed: {e}")
        raise e

