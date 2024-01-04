# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }



import json
import boto3

# Bedrock client used to interact with APIs around models
bedrock = boto3.client(
  service_name='bedrock', 
  region_name='us-east-1'
)

# Bedrock Runtime client used to invoke and question the models
bedrock_runtime = boto3.client(
  service_name='bedrock-runtime', 
  region_name='us-east-1'
)

def handler(event, context):
  incoming = json.loads(event.get("body"))

  idea_prompt = "a poster created with {analog} and {digital}".format(incoming.get("analog"), incoming.get("digital"))

  # The payload to be provided to Bedrock 
  body = json.dumps({
    "prompt": prompt, 
    "maxTokens": 200,
    "temperature": 0.7,
    "topP": 1,
  })

  # The actual call to retrieve an answer from the model
  response = bedrock_runtime.invoke_model(
    body=body, 
    modelId="amazon.titan-image-generator-v1", 
    accept='application/json', 
    contentType='application/json'
  )

  response_body = json.loads(response.get('body').read())

  # The response from the model now mapped to the answer
  resp = response_body.get('completions')[0].get('data')

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(resp) # TODO: return the image url?
  }