# GradioとAmazon Bedrockの統合プロジェクト

このプロジェクトは、Gradioを利用したシンプルなフロントエンドインターフェースを提供し、Amazon Bedrock APIを用いてモデル推論を実施するためにスクラッチで構築されています。

## プロジェクト構成

- **README.md**: プロジェクトの説明およびドキュメント。
- **requirements.txt**: Pythonの依存パッケージ一覧。
- **config/config.json**: Amazon Bedrockの設定ファイル。  
  BedrockのAPIエンドポイントおよびAPIキーを記載してください。
- **src/frontend.py**: Gradioを使用したフロントエンドの実装。  
  ユーザーの入力を受け取り、モデルへの問い合わせを行い、結果を表示します。
- **src/bedrock.py**: Amazon Bedrockとの通信処理を担当。  
  設定ファイルから情報を読み取り、APIリクエストを送信します。  
  エンドポイントが設定されていない場合はシミュレートされた応答を返します。

## セットアップ

1. 必要なパッケージをインストールしてください:
   ```
   pip install -r requirements.txt
   ```

2. `config/config.json` を、ご自身のAmazon Bedrockの設定に合わせて更新してください:
   ```json
   {
       "bedrock_endpoint": "YOUR_BEDROCK_ENDPOINT",
       "api_key": "YOUR_API_KEY"
   }
   ```

3. Gradioインターフェイスを起動します:
   ```
   python src/frontend.py
   ```

## 使用方法

GradioのUIに表示されるテキストボックスに問い合わせ内容を入力してください。入力は `src/bedrock.py` を介してAmazon Bedrockに送信され、結果が画面に表示されます。

## 注意点

- `bedrock_endpoint` が設定されていない場合、シミュレートされた応答が返されます。
- API認証情報およびネットワーク設定が正しく構成されていることを確認してください。

どうぞご利用ください。
