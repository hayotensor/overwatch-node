from datasets import load_dataset

class MATH:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("math_dataset", split="train")

    def run(self, num_samples=10):
        """Evaluate mathematical reasoning."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["question"])
            results.append({"problem": item["question"], "expected": item["answer"], "actual": response})
        return results
