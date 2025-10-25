import json
import random
from typing import List, Dict

# Load your TechNova dataset
with open('technova_dataset.json', 'r') as f:
    technova_data = json.load(f)

def format_for_openai_chat(data: List[Dict], system_prompt: str = None) -> List[Dict]:
    """
    Format data for OpenAI Chat Completions fine-tuning.
    Compatible with GPT-3.5-turbo and GPT-4 fine-tuning.
    """
    if system_prompt is None:
        system_prompt = """You are a TechNova Solutions support agent. Your role is to classify customer support tickets and provide structured responses with the following information:
- category: Specific issue category (Product-IssueType format)
- priority: Critical, High, Medium, or Low
- product: Which TechNova product (DataSync Pro, AnalyticsPulse, SecureVault, CloudBridge, or WorkflowMax)
- action: Specific troubleshooting steps or actions to take
- escalate_to: Which team should handle this
- estimated_resolution: Expected time to resolve

Always respond with valid JSON format."""
    
    formatted_data = []
    
    for example in data:
        formatted_example = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": example["input"]
                },
                {
                    "role": "assistant",
                    "content": json.dumps(example["output"], indent=2)
                }
            ]
        }
        formatted_data.append(formatted_example)
    
    return formatted_data


def format_for_openai_completion(data: List[Dict]) -> List[Dict]:
    """
    Format data for OpenAI legacy Completions fine-tuning.
    (For older models like davinci, curie - mostly deprecated)
    """
    formatted_data = []
    
    for example in data:
        formatted_example = {
            "prompt": f"Classify this TechNova support ticket:\n\n{example['input']}\n\n###\n\n",
            "completion": f" {json.dumps(example['output'], indent=2)}###"
        }
        formatted_data.append(formatted_example)
    
    return formatted_data


def create_train_test_split(data: List[Dict], train_ratio: float = 0.8, shuffle: bool = True):
    """
    Split data into training and testing sets.
    """
    if shuffle:
        data_copy = data.copy()
        random.seed(42)  # For reproducibility
        random.shuffle(data_copy)
    else:
        data_copy = data
    
    split_idx = int(len(data_copy) * train_ratio)
    train_data = data_copy[:split_idx]
    test_data = data_copy[split_idx:]
    
    return train_data, test_data


def save_for_openai_finetuning(train_data: List[Dict], test_data: List[Dict], 
                                output_dir: str = "."):
    """
    Save formatted data in JSONL format required by OpenAI.
    Each line is a separate JSON object.
    """
    # Save training data
    train_file = f"{output_dir}/technova_train.jsonl"
    with open(train_file, 'w') as f:
        for example in train_data:
            f.write(json.dumps(example) + '\n')
    
    # Save test/validation data
    test_file = f"{output_dir}/technova_test.jsonl"
    with open(test_file, 'w') as f:
        for example in test_data:
            f.write(json.dumps(example) + '\n')
    
    print(f"✓ Training data saved to: {train_file}")
    print(f"  → {len(train_data)} examples")
    print(f"✓ Test data saved to: {test_file}")
    print(f"  → {len(test_data)} examples")
    
    return train_file, test_file


def validate_openai_format(data: List[Dict]) -> bool:
    """
    Validate that data meets OpenAI fine-tuning requirements.
    """
    errors = []
    
    for idx, example in enumerate(data):
        # Check required structure
        if "messages" not in example:
            errors.append(f"Example {idx}: Missing 'messages' key")
            continue
        
        messages = example["messages"]
        
        # Check message structure
        if len(messages) < 2:
            errors.append(f"Example {idx}: Need at least 2 messages (user + assistant)")
        
        # Check roles
        roles = [msg.get("role") for msg in messages]
        if "user" not in roles or "assistant" not in roles:
            errors.append(f"Example {idx}: Missing user or assistant role")
        
        # Check content
        for msg_idx, msg in enumerate(messages):
            if "content" not in msg or not msg["content"]:
                errors.append(f"Example {idx}, Message {msg_idx}: Missing or empty content")
    
    if errors:
        print("❌ Validation failed:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        return False
    else:
        print("✓ Validation passed!")
        print(f"  → {len(data)} examples are properly formatted")
        return True


def estimate_training_cost(num_examples: int, avg_tokens_per_example: int = 150, 
                          model: str = "gpt-3.5-turbo"):
    """
    Estimate the cost of fine-tuning on OpenAI.
    Prices as of 2024 (check OpenAI pricing page for latest).
    """
    costs_per_1k_tokens = {
        "gpt-3.5-turbo": 0.008,  # Training cost
        "gpt-4o-mini": 0.008,
    }
    
    if model not in costs_per_1k_tokens:
        print(f"⚠️  Unknown model: {model}")
        return None
    
    total_tokens = num_examples * avg_tokens_per_example
    cost = (total_tokens / 1000) * costs_per_1k_tokens[model]
    
    # Typically need 3-4 epochs
    epochs = 3
    total_cost = cost * epochs
    
    print(f"\n💰 Estimated Training Cost for {model}:")
    print(f"  → Examples: {num_examples}")
    print(f"  → Estimated tokens: {total_tokens:,}")
    print(f"  → Cost per epoch: ${cost:.2f}")
    print(f"  → Total cost (~{epochs} epochs): ${total_cost:.2f}")
    
    return total_cost


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("TechNova Dataset → OpenAI Fine-Tuning Format")
    print("=" * 60)
    
    # 1. Format the data for OpenAI Chat Completions
    print("\n📝 Formatting data for OpenAI Chat Completions...")
    formatted_data = format_for_openai_chat(technova_data)
    
    # 2. Validate format
    print("\n🔍 Validating format...")
    is_valid = validate_openai_format(formatted_data)
    
    if not is_valid:
        print("\n⚠️  Please fix validation errors before proceeding.")
        exit(1)
    
    # 3. Create train/test split
    print("\n✂️  Splitting data (80% train, 20% test)...")
    train_data, test_data = create_train_test_split(formatted_data, train_ratio=0.8)
    
    # 4. Save to JSONL files
    print("\n💾 Saving files...")
    train_file, test_file = save_for_openai_finetuning(train_data, test_data)
    
    # 5. Estimate cost
    estimate_training_cost(len(train_data), model="gpt-3.5-turbo")
    
    print("\n" + "=" * 60)
    print("✨ Next Steps:")
    print("=" * 60)
    print("\n1. Upload training file to OpenAI:")
    print(f"   openai api files create -f {train_file} -p fine-tune")
    print("\n2. Create fine-tuning job:")
    print("   openai api fine_tuning.jobs.create \\")
    print("     -t <TRAINING_FILE_ID> \\")
    print("     -m gpt-3.5-turbo \\")
    print("     --suffix 'technova-support'")
    print("\n3. Monitor training:")
    print("   openai api fine_tuning.jobs.get -i <JOB_ID>")
    print("\n4. Use your fine-tuned model:")
    print("   Model name: ft:gpt-3.5-turbo:...:technova-support:...")
    print("\n" + "=" * 60)
    
    # Optional: Show a sample
    print("\n📄 Sample formatted example:")
    print(json.dumps(formatted_data[0], indent=2)[:500] + "...")