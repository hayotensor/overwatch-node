from benchmark_manager import BenchmarkManager

# Mock AI Model
class MockModel:
    def generate(self, prompt):
        return f"Generated response for: {prompt}"

if __name__ == "__main__":
    model = MockModel()
    benchmark_manager = BenchmarkManager(model)
    results = benchmark_manager.run_all(num_samples=5)

    for benchmark, result in results.items():
        print(f"\nResults for {benchmark}:")
        for entry in result:
            print(entry)
