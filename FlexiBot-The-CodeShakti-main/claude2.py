## Exam
importboto3
import json
# Input prompt
prompt_data = "Act as Shakespeare and write a poem on machine learning."

# Create a Bedrock Runtime client in us-east-1
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Payload for invoking the Claude model
payload = {
    "prompt": f"\n\nHuman: {prompt_data}\n\nAssistant:",
    "max_tokens_to_sample": 512,  # Maximum number of tokens to generate
    "temperature": 0.5,           # Controls randomness (lower = more deterministic)
    "top_k": 250,                 # Controls diversity (lower = more focused)
    "top_p": 0.9,                 # Controls diversity (lower = more focused)
    "stop_sequences": ["\n\nHuman:"],
    "anthropic_version": "bedrock-2023-05-31"
}

# Convert payload to JSON string
body = json.dumps(payload)

# Model ID for Claude v2
model_id = "anthropic.claude-v2:1"

try:
    # Invoke the model
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    # Parse the response
    response_body = json.loads(response.get("body").read())
    response_text = response_body['completion']  # Claude uses 'completion' instead of 'generation'
    print(response_text)

except bedrock.exceptions.AccessDeniedException as e:
    print(f"Access Denied: {e}")
    print("Ensure that your IAM role or user has the necessary permissions to invoke the model.")
    print("Also, verify that the model is available in your AWS account and region.")

except Exception as e:
    print(f"An error occurred: {e}")