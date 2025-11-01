import json

from dotenv import load_dotenv
load_dotenv()

from langsmith import Client, wrappers
from langsmith.schemas import Example, Run
ls_client = Client()

from openai import OpenAI
openai_client = wrappers.wrap_openai(OpenAI())

def gpt_4o_mini_runner(inputs: dict) -> dict:
    model="gpt-4o-mini-2024-07-18"
    return runner(model, inputs)

def gpt_5_chat_runner(inputs: dict) -> dict:
    model="gpt-5-chat-latest"
    return runner(model, inputs)

def fine_tuned_runner(inputs: dict) -> dict:
    model="ft:gpt-4o-mini-2024-07-18:oguzhan-cetinkaya:technova-agent:CUOO1qJB"
    return runner(model, inputs)

def runner(model, inputs: dict) -> dict:
    system_prompt = """
You are a TechNova Solutions support agent. Your role is to classify customer support tickets and provide structured responses with the following information:
- category: Specific issue category (Product-IssueType format)
- priority: Critical, High, Medium, or Low
- product: Which TechNova product (DataSync Pro, AnalyticsPulse, SecureVault, CloudBridge, or WorkflowMax)
- action: Specific troubleshooting steps or actions to take
- escalate_to: Which team should handle this
- estimated_resolution: Expected time to resolve

Always respond with valid JSON format.""".strip()
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": inputs["inputs_1"]},
        ],
    )
    return {"output": response.choices[0].message.content}

def evaluator(run: Run, example: Example):
    notes = ""
    score = 0

    prediction = run.outputs["output"]
    prediction = json.loads(prediction.replace("```json","").replace("\n","").replace("```",""))
    reference = json.loads(example.outputs["outputs_1"])
    user_input = example.inputs["inputs_1"]

    # category
    if "category" in prediction:
        if prediction["category"] == reference["category"]:
            score += 10
            notes += "Category match. +10\n"
        else:
            notes += f"Category mismatch. Expected: {reference['category']}, Got: {prediction['category']}\n"
    
    # priority
    if "priority" in prediction:
        if prediction["priority"] == reference["priority"]:
            score += 10
            notes += "Priority match. +10\n"
        else:
            notes += f"Priority mismatch. Expected: {reference['priority']}, Got: {prediction['priority']}\n"
    
    # product
    if "product" in prediction:
        if prediction["product"] == reference["product"]:
            score += 10
            notes += "Product match. +10\n"
        else:
            notes += f"Product mismatch. Expected: {reference['product']}, Got: {prediction['product']}\n"

    # escalate_to
    if "escalate_to" in prediction:
        if prediction["escalate_to"] == reference["escalate_to"]:
            score += 10
            notes += "Escalate_to match. +10\n"
        else:
            notes += f"Escalate_to mismatch. Expected: {reference['escalate_to']}, Got: {prediction['escalate_to']}\n"

    # estimated_resolution
    if "estimated_resolution" in prediction:
        if prediction["estimated_resolution"] == reference["estimated_resolution"]:
            score += 10
            notes += "Estimated_resolution match. +10\n"
        else:
            notes += f"Estimated_resolution mismatch. Expected: {reference['estimated_resolution']}, Got: {prediction['estimated_resolution']}\n"
  
    # action
    if "action" in prediction:
        ai_score, ai_notes = judge_action_with_ai(prediction["action"], reference["action"])
        score += ai_score
        notes += f"AI SCORE: {ai_score}/50\nAI NOTES: {ai_notes}\n"

    return {"score": score, "notes": notes.strip()}
  
def judge_action_with_ai(prediction_action, reference_action):
    ai_judge_prompt = f"""
    You are an expert evaluator. 
    Given the reference action and the predicted action for a TechNova support ticket, assess the quality of the predicted action.

    Evaluate based on the following criteria:
    1. Completeness: Does the predicted action cover all necessary steps mentioned in the reference action?
    2. Accuracy: Are the steps in the predicted action correct and relevant to the issue described?
    3. Clarity: Is the predicted action clearly articulated and easy to understand?

    Scoring(0-50):
    45-50: Same meaning, all steps match.
    35-44: Minor rewording or small omission.
    25-34: Partial overlap, key step missing.
    10-24: Limited similarity.
    0-9: Unrelated or incorrect.

    Output JSON only: {{"score": <0-50>, "reason": "<short reason>"}}

    Reference: {reference_action}
    Prediction: {prediction_action}
    """.strip()

    response = openai_client.chat.completions.create(
        model="gpt-5-chat-latest",
        messages=[
            {"role": "system", "content": ai_judge_prompt}
        ],
    )

    result = json.loads(response.choices[0].message.content)
    ai_score = result["score"]
    ai_notes = result["reason"]

    return ai_score, ai_notes

ls_client.evaluate(
    fine_tuned_runner,
    data="ds-frosty-sundial-68",
    evaluators=[evaluator],
    experiment_prefix="finetuned",
    max_concurrency=4,
    description="Evaluation of TechNova support ticket classification and response generation.",
)