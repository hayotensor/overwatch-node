from datasets import load_dataset

class MuSR:
    def __init__(self, model):
        self.model = model
        self.dataset = load_dataset("gsm8k", split="train")

    def run(self, num_samples=10):
        """Multistep reasoning evaluation."""
        results = []
        for item in self.dataset.select(range(num_samples)):
            response = self.model.generate(item["question"])
            results.append({"prompt": item["question"], "expected": item["answer"], "actual": response})
        return results
