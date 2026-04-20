import boto3
import json

ses = boto3.client('ses')

def lambda_handler(event, context):
    # 1. Parse the message from the website
    try:
        body = json.loads(event['body'])
        visitor_message = body.get('message', 'No message provided')
    except:
        visitor_message = "Error: Could not parse message body."

    SENDER = "mayankwakdikar+aws@gmail.com" # Must be verified in SES
    RECIPIENT = "mayankwakdikar+aws@gmail.com"
    
    # 2. Construct the Email
    response = ses.send_email(
        Destination={'ToAddresses': [RECIPIENT]},
        Message={
            'Body': {
                'Text': {
                    'Data': f"New Portfolio Message:\n\n{visitor_message}"
                }
            },
            'Subject': {'Data': "Portfolio Contact Form Notification"},
        },
        Source=SENDER
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'status': 'Email sent successfully!'})
    }