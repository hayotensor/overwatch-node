from datasets import load_dataset

class GPQA:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("truthful_qa", split="validation")

    def run(self, num_samples=10):
        """Evaluate Graduate-Level QA."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["question"])
            results.append({"query": item["question"], "expected": item["best_answer"], "actual": response})
        return results
