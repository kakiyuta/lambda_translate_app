import json
import urllib.parse
import boto3
import datetime

print('Loading function')

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        
        result = transcribe.start_transcription_job(
            TranscriptionJobName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_Transcription',
            LanguageCode = 'en-US',
            Media = {
                'MediaFileUri': 'https://s3.ap-northeast-1.amazonaws.com/' + bucket + '/' + key
            },
            OutputBucketName = '20200406-transcribe-output-yourname'
        )
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
