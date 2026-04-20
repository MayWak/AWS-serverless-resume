import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-counter') # Make sure this matches your table name exactly

def lambda_handler(event, context):
    # 1. Update the 'count' for the item where id is 'visitors'
    # This 'ADD' operation is atomic, meaning it prevents race conditions
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD #c :val',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':val': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    # 2. Extract the new count from the response
    new_count = str(response['Attributes']['count'])
    
    # 3. Return the response with CORS headers (Critical for your website)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*', # Allows your CloudFront URL to talk to this API
            'Access-Control-Allow-Methods': 'GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'count': new_count})
    }