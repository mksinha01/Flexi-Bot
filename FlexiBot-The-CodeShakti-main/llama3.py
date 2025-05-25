import boto3 #aws Software Development Kit
import json 

# Input prompt
prompt_data = "Act as Shakespeare and write a poem on machine learning."

# Create a Bedrock Runtime client in us-east-1 , AWS Bedrock Runtime service ka ek client banata
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Payload for invoking the model ,  ek dictionary hai jo model ko invoke karne ke liye required parameters ko define karta hai
payload = {
    "prompt": prompt_data,
    "max_gen_len": 512,  # Maximum number of tokens to generate
    "temperature": 0.5,  # Controls randomness (lower = more deterministic)
    "top_p": 0.9         # Controls diversity (lower = more focused)
}
body = json.dumps(payload)

# Model ID for Llama 3 70B Instruct
model_id = "meta.llama3-70b-instruct-v1:0"

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
    response_text = response_body['generation']
    print(response_text)

except bedrock.exceptions.AccessDeniedException as e:
    print(f"Access Denied: {e}")
    print("Ensure that your IAM role or user has the necessary permissions to invoke the model.")
    print("Also, verify that the model is available in your AWS account and region.")

except Exception as e:
    print(f"An error occurred: {e}")