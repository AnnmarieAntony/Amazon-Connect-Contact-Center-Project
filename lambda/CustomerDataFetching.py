import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Customers')


def lambda_handler(event, context):
    # TODO implement
    Phone = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    print(Phone)
    response =table.query(
        IndexName='PhoneNumber',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('PhoneNumber').eq(Phone)
    )
       
    print(response['Items'])
    if len(response['Items'])>0:
        greeting = 'Hello ' + response['Items'][0]['FirstName']+" Thanks for Calling our It support"
    else:
        greeting = "Thanks for calling our IT support"
    print (greeting)
     
    return {
        'statusCode': 200,
        'body': greeting
    }
