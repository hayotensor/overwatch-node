from datasets import load_dataset

class IFEval:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("tatsu-lab/alpaca", split="train")

    def run(self, num_samples=10):
        """Evaluate model on real instruction-following dataset."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["instruction"])
            results.append({"instruction": item["instruction"], "expected": item["output"], "actual": response})
        return results
