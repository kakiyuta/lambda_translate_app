import json
import boto3
import datetime
import time

def lambda_handler(event, context):
    
    translate = boto3.client('translate')
    dynamodb = boto3.client('dynamodb')
    input_text = event['queryStringParameters']['input_text']
    
    response = translate.translate_text(
        Text=input_text,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )
    
    output_text = response.get('TranslatedText')
    
    # 翻訳履歴をDynamoDBに保存
    item = {
        "from": {"S": input_text},
        "to": {"S": output_text},
        "translated_at": {"S": datetime.datetime.now().isoformat(' ')},
        "timestamp": {"N": str(int(time.time()))}
    }
    dynamodb.put_item(
        TableName = "TranslateHistories",
        Item = item
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'output_text': output_text
        })
    }
