# Client モジュール

`client.py` には、トレース操作を行うための `EvalTrackClient` クラスが定義されています。

## EvalTrackClient クラス

トレースデータの取得と保存を行うためのクライアントクラス。

### メソッド

#### get_traces()
トレースデータを取得します。

**戻り値**:
- `dict`: 取得したトレースデータ
  - エラー時は空の辞書 `{}` を返します

**使用例**:
```python
from tracker.client import EvalTrackClient

client = EvalTrackClient()
traces = client.get_traces()
```

#### put_trace(trace_id: str, data: dict)
トレースデータを保存します。

**引数**:
- `trace_id` (str): トレースの一意識別子
- `data` (dict): 保存するトレースデータ

**戻り値**:
- `None`

**使用例**:
```python
from tracker.client import EvalTrackClient

client = EvalTrackClient()
client.put_trace("trace-123", {"request": "...", "response": "..."})
```

### エラーハンドリング
- HTTP リクエストが失敗した場合（ステータスコードが 200 以外）はエラーログを出力
- 予期せぬエラーが発生した場合もエラーログを出力
