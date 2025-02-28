from benchmarks.ifeval import IFEval
from benchmarks.bbh import BBH
from benchmarks.math import MATH
from benchmarks.gpqa import GPQA
from benchmarks.musr import MuSR
from benchmarks.mmlu_pro import MMLUPro

class BenchmarkManager:
    def __init__(self, model):
        self.model = model
        self.benchmarks = {
            "IFEval": IFEval(model),
            "BBH": BBH(model),
            "MATH": MATH(model),
            "GPQA": GPQA(model),
            "MuSR": MuSR(model),
            "MMLU-Pro": MMLUPro(model),
        }

    def run_all(self, num_samples=10):
        """Runs all benchmarks and returns results."""
        results = {}
        for name, benchmark in self.benchmarks.items():
            print(f"Running {name} benchmark...")
            results[name] = benchmark.run(num_samples)
        return results
