from datasets import load_dataset

class MMLUPro:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("ai2_arc", split="test")

    def run(self, num_samples=10):
        """Professional-level multitask understanding."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["question"])
            results.append({"task": item["question"], "expected": item["answer"], "actual": response})
        return results
