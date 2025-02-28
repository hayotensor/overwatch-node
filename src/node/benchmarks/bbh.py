from datasets import load_dataset

class BBH:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("stanford-crfm/bigbench-hard", split="train")

    def run(self, num_samples=10):
        """Evaluate model on Big Bench Hard dataset."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["inputs"])
            results.append({"question": item["inputs"], "expected": item["targets"], "actual": response})
        return results
