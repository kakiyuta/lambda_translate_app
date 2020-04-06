import json
import urllib.parse
import boto3
import datetime
import re

s3 = boto3.resource('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    pattern = re.compile('\d{14}_Transcription.json')
    try:
        match_result = pattern.match(key)
        if not match_result:
            # 翻訳対象のファイルではないため
            print("Uploading file is not target file of translate")
            return
        
        # s3のJSONファイルから翻訳対象の文字列を抽出
        s3_obj = s3.Object(bucket, key)
        file_content = s3_obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        input_text = json_content.get('results').get('transcripts')[0].get('transcript')
        print("translation target : " + input_text)
        
        # 翻訳
        response = translate.translate_text(
            Text=input_text,
            SourceLanguageCode='en',
            TargetLanguageCode='ja'
        )
        output_text = response.get('TranslatedText')
        
        # 翻訳結果をS3ファイルに書き込み
        write_object = s3.Object(bucket, 'translated/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_translated.txt")
        write_object.put(Body=output_text)

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
