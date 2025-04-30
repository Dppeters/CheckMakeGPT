import pandas as pd
from datetime import datetime
from core.tester import CustomGPTTester
from core.evaluator import SalesEvaluator
from config import config
import time


def load_prompts() -> list:
    """Load test prompts from prompts/ directory"""
    try:
        with open(f"{config.PROMPT_DIR}/sales_prompts.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        default_prompts = [
            "How much does a pool installation cost?",
            "What are the benefits of saltwater pools?"
        ]
        with open(f"{config.PROMPT_DIR}/sales_prompts.txt", "w") as f:
            f.write("\n".join(default_prompts))
        return default_prompts


def test_agents(agent_names: list = None):
    """Run tests against specified agents"""
    agent_names = agent_names or list(config.AGENTS.keys())
    results = []

    for agent_name in agent_names:
        tester = CustomGPTTester(agent_name)
        print(f"\nTesting Agent: {agent_name}")

        for prompt in load_prompts():
            print(f"  Prompt: {prompt[:60]}...")
            test_result = tester.test_prompt(prompt)

            if test_result["success"]:
                evaluation = SalesEvaluator.evaluate(test_result["response"])
                results.append({
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_name,
                    "agent_id": test_result["agent_id"],
                    "prompt": prompt,
                    "response": test_result["response"],
                    **evaluation
                })
            else:
                print(f"  ERROR: {test_result['error']}")

            time.sleep(1)  # Rate limiting

    save_results(results)


def save_results(data: list):
    """Save results to timestamped CSV"""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame(data)
    csv_path = f"{config.OUTPUT_DIR}/results_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nResults saved to: {csv_path}")


if __name__ == "__main__":
    # Example: Test specific agents
    test_agents(["primary"])  # Or test_agents() for all agents