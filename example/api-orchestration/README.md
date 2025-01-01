# [Example]: API Orchestration

このサンプルは、複数のマイクロサービス間での eval-track の使用方法を示します。EvalTrackClient と capture_response デコレータを使用して、サービス間の通信を追跡する方法を実演します。

## 実行方法

```bash
git clone https://github.com/tied-inc/eval-track
cd example/api-orchestration
uv sync --frozen
uv main:app
```

## エンドポイント

このアプリケーションには以下のエンドポイントが含まれています：

### eval-track 基本エンドポイント
- `GET /eval-track/health`
- `GET /eval-track/traces`
- `PUT /eval-track/traces/{trace_id}`

### サービスエンドポイント
- `GET /service1` - 第1マイクロサービスのデモ
- `GET /service2` - 第2マイクロサービスのデモ
- `GET /orchestrate` - サービス間連携のデモ

## 機能説明

1. **マイクロサービス** (`/service1`, `/service2`)
   - 独立したサービスのシミュレーション
   - 非同期処理の実装例
   - @capture_response デコレータによるトレース取得

2. **オーケストレーション** (`/orchestrate`)
   - 複数サービスの並列呼び出し
   - エラーハンドリング
   - トレースの集約と表示

## 使用方法

1. eval-track をインストール:
   ```bash
   uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
   ```

2. アプリケーションを実行:
   ```bash
   uvicorn main:app --reload
   ```

3. エンドポイントをテスト:
   ```bash
   # 個別サービスのテスト
   curl http://localhost:8000/service1
   curl http://localhost:8000/service2

   # オーケストレーションのテスト
   curl http://localhost:8000/orchestrate
   ```

4. トレースを確認:
   ```bash
   curl http://localhost:8000/eval-track/traces
   ```

## 実装の詳細

このサンプルでは以下の機能を実演しています：

1. **EvalTrackClient の使用**
   - トレースデータの取得と保存
   - 複数サービスからのトレースの集約

2. **@capture_response デコレータ**
   - 非同期関数でのトレース取得
   - エラー発生時のトレース取得

3. **サービス間通信**
   - httpx を使用した非同期HTTP通信
   - 並列リクエストの処理
   - エラーハンドリングとリカバリー

詳細な実装については [main.py](./main.py) を参照してください。
