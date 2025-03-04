from datasets import load_dataset
from agieval import AGIEval

"""
A simplified and quicker version of benchmarking 
"""
class AGIEvalBenchmark:
    def __init__(self, model, tokenizer, task="mmlu"):
        """Initialize AGIEval with a specific task."""
        self.model = model
        self.tokenizer = tokenizer
        self.agieval = AGIEval(model, tokenizer, task=task)

    def run(self, num_samples=10):
        """Run AGIEval on a subset of samples."""
        results = self.agieval.run(num_samples=num_samples)
        return results
