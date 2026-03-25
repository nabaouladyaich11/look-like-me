# similarity.py  — place at LOOK_LIKE_ME/ root
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class SimilarityResult:
    rank:       int     # 1 = most similar
    gallery_id: str     # e.g. 'gallery_1'
    img_path:   str     # full path to the gallery image
    score:      float   # cosine similarity score: 0.0 -> 1.0


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes cosine similarity between two L2-normalized unit vectors.
    Because both vectors are already normalized, this is just the dot product.

    Args:
        a, b : 1D numpy arrays of shape (4096,), already L2-normalized
    Returns:
        float in range [-1.0, 1.0]  — in practice [0.0, 1.0] for faces
    """
    return float(np.dot(a, b))


def rank_gallery(
    query_embedding:   np.ndarray,
    gallery_embeddings: List[np.ndarray],
    gallery_ids:        List[str],
    gallery_paths:      List[str],
    top_k: int = 3,
) -> List[SimilarityResult]:
    """
    Compares one query embedding against all gallery embeddings,
    sorts by cosine similarity descending, and returns the Top-K results.

    Args:
        query_embedding    : shape (4096,) — from the query image
        gallery_embeddings : list of N arrays, each shape (4096,)  
        gallery_ids        : list of N strings (e.g. ['gallery_1', ...])
        gallery_paths      : list of N image file paths
        top_k              : how many top results to return (default 3)
    Returns:
        list of SimilarityResult sorted by score descending, length = top_k
    """
    scores = [
        cosine_similarity(query_embedding, g_emb)
        for g_emb in gallery_embeddings
    ]

    # Pair each score with its metadata and sort highest first
    paired = list(zip(scores, gallery_ids, gallery_paths))
    paired.sort(key=lambda x: x[0], reverse=True)

    results = [
        SimilarityResult(
            rank       = i + 1,
            gallery_id = gid,
            img_path   = gpath,
            score      = score,
        )
        for i, (score, gid, gpath) in enumerate(paired[:top_k])
    ]
    return results
