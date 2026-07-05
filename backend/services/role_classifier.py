class RoleClassifier:

    def classify(self, text: str) -> str:
        """
        Lightweight deterministic role classifier.
        No LLM needed (fast + stable).
        """

        text = text.lower()

        # ---------------- FULL STACK ----------------
        full_stack_signals = [
            "react", "node", "express", "frontend", "backend",
            "full stack", "javascript", "typescript", "rest api"
        ]

        # ---------------- DATA SCIENCE ----------------
        ds_signals = [
            "machine learning", "deep learning", "tensorflow",
            "pytorch", "pandas", "numpy", "scikit-learn",
            "nlp", "data science", "statistics"
        ]

        # ---------------- DEVOPS ----------------
        devops_signals = [
            "docker", "kubernetes", "terraform", "ci/cd",
            "aws", "gcp", "azure", "jenkins", "devops",
            "microservices", "linux"
        ]

        fs_score = sum(1 for w in full_stack_signals if w in text)
        ds_score = sum(1 for w in ds_signals if w in text)
        dv_score = sum(1 for w in devops_signals if w in text)

        if ds_score >= fs_score and ds_score >= dv_score:
            return "data_science"

        if dv_score > fs_score:
            return "devops"

        if fs_score > 0:
            return "full_stack"

        return "general"