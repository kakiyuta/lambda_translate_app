# AWS Lambda 翻訳アプリ

## 概要

AWS Lambdaの学習で以下のサイトを参考に翻訳アプリケーションを作成
https://speakerdeck.com/ketancho/jaws-ug-bgnr-24-serverless-quick-start-hands-on

## 各ファイルの説明

### translate-function.py

APIのGETをから翻訳対処の文字列を受け取り、翻訳結果をJSONで返す関数。
翻訳履歴はDynamoDBに保存される

### transcribe-function.py

S3から音声データを受け取り、`transcribe` サービスを利用して文字起こしを行う関数。
文字起こしした結果は別のS3バケットに出力する。

## translate-function-from-s3.py

`translate-function.py` はAPIからキックされるのに対して、こっちはS3にファイルがアップロードされたら開始する翻訳関数。
翻訳した結果はテキストファイルとしてS3のバケットに出力する。
基本的には`transcribe-function.py` から文字起こしされた英語のテキストを日本語に翻訳するために用いる。