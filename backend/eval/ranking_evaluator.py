import numpy as np


class RankingEvaluator:

    def __init__(self):
        pass

    # -----------------------------
    # Precision@K
    # -----------------------------
    def precision_at_k(self, ranked_list, relevant_set, k=10):
        top_k = ranked_list[:k]
        if not top_k:
            return 0.0

        hits = sum(1 for c in top_k if c in relevant_set)
        return round(hits / k, 3)

    # -----------------------------
    # Recall@K
    # -----------------------------
    def recall_at_k(self, ranked_list, relevant_set, k=10):
        if not relevant_set:
            return 0.0

        top_k = ranked_list[:k]
        hits = sum(1 for c in top_k if c in relevant_set)
        return round(hits / len(relevant_set), 3)

    # -----------------------------
    # DCG helper
    # -----------------------------
    def dcg(self, rels):
        return sum(rel / np.log2(idx + 2) for idx, rel in enumerate(rels))

    # -----------------------------
    # NDCG@K
    # -----------------------------
    def ndcg_at_k(self, ranked_list, relevant_set, k=10):
        top_k = ranked_list[:k]

        rels = [1 if c in relevant_set else 0 for c in top_k]
        dcg_val = self.dcg(rels)

        ideal_rels = sorted(rels, reverse=True)
        idcg = self.dcg(ideal_rels)

        if idcg == 0:
            return 0.0

        return round(dcg_val / idcg, 3)

    # -----------------------------
    # FULL REPORT
    # -----------------------------
    def evaluate(self, ranked_candidates, ground_truth, k=10):

        ranked_ids = [c["candidate_id"] for c in ranked_candidates]

        return {
            "precision@k": self.precision_at_k(ranked_ids, ground_truth, k),
            "recall@k": self.recall_at_k(ranked_ids, ground_truth, k),
            "ndcg@k": self.ndcg_at_k(ranked_ids, ground_truth, k),
            "k": k
        }


evaluator = RankingEvaluator()