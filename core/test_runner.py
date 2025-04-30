import os
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from config import config
from core.tester import CustomGPTTester
from core.openai_evaluator import OpenAIScorer


def run_tests():
    """Main test execution with comprehensive logging"""
    print("🚀 Starting CustomGPT Evaluation Run")
    start_time = time.time()

    try:
        # Initialize components
        tester = CustomGPTTester()
        scorer = OpenAIScorer()

        # Load and validate prompts
        prompts = config.prompts
        print(f"📋 Loaded {len(prompts)} test prompts")

        # Process prompts
        results = []
        for i, prompt in enumerate(prompts, 1):
            test_data = process_prompt(i, prompt, tester, scorer)
            results.append(test_data)
            time.sleep(config.API_COOLDOWN)

        # Save and verify results
        output_files = save_results(results)
        print("\n✅ Evaluation Metrics:")
        print_metrics(results)

        print(f"\n⏱️  Total execution time: {time.time() - start_time:.2f}s")
        print(f"📊 Results saved to:\n- {output_files['json']}\n- {output_files['csv']}")

    except Exception as e:
        print(f"\n❌ Critical failure: {str(e)}")
        raise


def process_prompt(index, prompt, tester, scorer):
    """Process a single prompt with detailed logging"""
    print(f"\n🔍 [{index}/{len(config.prompts)}] Testing: {prompt[:50]}...")

    try:
        # Get CustomGPT response
        test_start = time.time()
        test_result = tester.test_prompt(prompt)
        test_time = time.time() - test_start

        if not test_result["success"]:
            raise RuntimeError(test_result["error"])

        # Evaluate with GPT-4
        eval_start = time.time()
        evaluation = scorer.evaluate(prompt, test_result["response"])
        eval_time = time.time() - eval_start

        print(f"   ✓ Response received in {test_time:.2f}s")
        print(f"   ✓ Evaluation completed in {eval_time:.2f}s")
        print(f"   ★ Overall score: {evaluation.get('overall_weighted_score', 'N/A')}/10")

        return {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": test_result["response"],
            "conversation_id": test_result.get("conversation_id"),
            "test_time_sec": round(test_time, 2),
            "eval_time_sec": round(eval_time, 2),
            "evaluation": evaluation
        }

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "error": str(e),
            "conversation_id": None
        }


def save_results(results):
    """Save results with robust verification"""
    outputs_dir = Path(config.OUTPUT_DIR).absolute()
    outputs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # JSON output
    json_path = outputs_dir / f"detailed_results_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # CSV output
    csv_path = outputs_dir / f"summary_{timestamp}.csv"
    csv_fields = [
        'timestamp', 'prompt', 'conversation_id',
        'test_time_sec', 'eval_time_sec',
        'overall_score', 'error'
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for r in results:
            writer.writerow({
                'timestamp': r['timestamp'],
                'prompt': r['prompt'][:120] + '...' if len(r['prompt']) > 120 else r['prompt'],
                'conversation_id': r.get('conversation_id', ''),
                'test_time_sec': r.get('test_time_sec', ''),
                'eval_time_sec': r.get('eval_time_sec', ''),
                'overall_score': r.get('evaluation', {}).get('overall_weighted_score', 'ERROR'),
                'error': r.get('error', '')
            })

    # Verify files
    if not (json_path.exists() and csv_path.exists()):
        raise RuntimeError("Failed to create output files")

    return {
        'json': str(json_path),
        'csv': str(csv_path)
    }


def print_metrics(results):
    """Print key performance metrics"""
    successful = [r for r in results if 'evaluation' in r]
    if not successful:
        print("⚠️ No successful evaluations to analyze")
        return

    avg_scores = {
        'Overall': sum(r['evaluation']['overall_weighted_score'] for r in successful) / len(successful),
        'Response Time': sum(r['test_time_sec'] for r in successful) / len(successful),
        'Evaluation Time': sum(r['eval_time_sec'] for r in successful) / len(successful)
    }

    print(f"• Average Overall Score: {avg_scores['Overall']:.1f}/10")
    print(f"• Avg Response Time: {avg_scores['Response Time']:.2f}s")
    print(f"• Avg Evaluation Time: {avg_scores['Evaluation Time']:.2f}s")
    print(f"• Success Rate: {len(successful)}/{len(results)} ({len(successful) / len(results) * 100:.0f}%)")


if __name__ == "__main__":
    run_tests()