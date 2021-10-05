import json
import base64

def lambda_handler(event, context):
    ## Print Event for Testing
    print(json.dumps(event))
    
    ## Check for password
    password = event['protocolData']['mqtt']['password']
    print("\n Base64 encoded Password is: "+ password)  
    password = str(base64.b64decode(password))
    password = password.replace("'","") 
    password = password.replace("b","", 1) 
    print("\n Base64 decoded Password is: "+ password)  
    
    ## If Password matches: continue, else: fail Authentication
    if password == "secret_password":
        print("Password Athentication: Success")
    else:
        print("Password Athentication: Failre")
        result = { 
        "isAuthenticated": False
        }
        return result

    ## Create Policy to limit access on what topics can be published on
    policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": [
        "arn:aws:iot:ap-south-1:*:client/${iot:ClientId}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:ap-south-1:*:topic/${iot:ClientId}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:ap-south-1:*:topicfilter/${iot:ClientId}/*"
      ]
    }
  ]
}
    result = { 
        "isAuthenticated": True, 
        "principalId":"EnhancedAuthorizerLambba", 
        "policyDocuments": [json.dumps(policy)],
        "disconnectAfterInSeconds": 1800,
        "refreshAfterInSeconds": 300
    }
    
    
    print(result)
    return result
