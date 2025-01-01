# Router モジュール

`router.py` には、トレースデータの API エンドポイントが定義されています。

## API エンドポイント

### GET /eval-track/health
ヘルスチェックエンドポイント。


**レスポンス**:
- `200 OK`: サービスが正常に動作している場合
- レスポンスボディ: `"OK"`

### GET /eval-track/traces
トレースデータ取得エンドポイント。

**レスポンス**:
- `200 OK`: トレースデータの取得に成功した場合
- レスポンスボディ: `{"message": "Logs endpoint"}`

### PUT /eval-track/traces/{trace_id}
トレースデータ保存エンドポイント。

**パスパラメータ**:
- `trace_id` (str): トレースの一意識別子

**リクエストボディ**:
- `data` (dict): 保存するトレースデータ

**レスポンス**:
- `204 No Content`: トレースデータの保存に成功した場合
- レスポンスボディ: なし

## ロギング

各エンドポイントは以下のようなログを出力します:

- ヘルスチェック: "Health check endpoint called"
- トレース取得: "Logs retrieval endpoint called"
- トレース保存: "Received logs with traceId: {trace_id}"

## 設定

- ルーターのプレフィックスは `/eval-track` に設定されています
- ロギングは NullHandler を使用して設定されています
