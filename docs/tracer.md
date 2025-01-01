# Tracer モジュール

`tracer.py` には、関数やコルーチンの応答をキャプチャするための `capture_response` デコレーターが定義されています。

## capture_response デコレーター

関数やコルーチンの戻り値を自動的にトレースデータとして記録するデコレーター。同期関数と非同期関数の両方に対応しています。

### 使用方法

```python
from tracker.tracer import capture_response
from pydantic import BaseModel

class Response(BaseModel):
    message: str

@capture_response
async def async_function() -> Response:
    return Response(message="Hello")

@capture_response
def sync_function() -> Response:
    return Response(message="World")
```

### 機能詳細

- ULID を使用して一意のトレース ID を生成
- FastAPI の BackgroundTasks を使用して非同期でトレースデータを保存
- 関数の戻り値は Pydantic の BaseModel である必要があります
- 元の関数のシグネチャと属性は @wraps によって保持されます

### 内部動作

1. デコレーターが適用されると、一意のトレース ID が生成されます
2. 関数が実行され、その戻り値が取得されます
3. BackgroundTasks を使用して、トレースデータが非同期で保存されます
4. 元の戻り値がそのまま返されます

### 対応している関数の種類

- 同期関数 (`def` で定義された通常の関数)
- 非同期関数 (`async def` で定義されたコルーチン)

### 制限事項

- 戻り値は必ず Pydantic の BaseModel を継承したクラスのインスタンスである必要があります
- トレースデータの保存は非同期で行われるため、即座には完了しない可能性があります
