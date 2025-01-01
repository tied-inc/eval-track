# [Example]: Advanced FastAPI Usage

このサンプルは、eval-track の高度な使用方法を示します。非同期処理、エラーハンドリング、そしてトレース機能の実践的な使い方を含んでいます。

## 実行方法

```bash
git clone https://github.com/tied-inc/eval-track
cd example/advanced-fastapi-usage
uv sync --frozen
uv main:app
```

## エンドポイント

このアプリケーションには以下のエンドポイントが含まれています：

### eval-track 基本エンドポイント
- `GET /eval-track/health`
- `GET /eval-track/traces`
- `PUT /eval-track/traces/{trace_id}`

### サンプルエンドポイント
- `GET /hello` - 基本的なトレース機能のデモ
- `GET /async-calc/{x}/{y}` - 非同期処理と計算のデモ
- `GET /error-demo` - エラーハンドリングのデモ

## 機能説明

1. **基本的なトレース機能** (`/hello`)
   - 同期関数でのトレース取得
   - Pydantic モデルを使用したレスポンス

2. **非同期計算** (`/async-calc/{x}/{y}`)
   - 非同期関数でのトレース取得
   - エラーハンドリング（ゼロ除算）
   - パスパラメータの使用例

3. **エラーハンドリング** (`/error-demo`)
   - HTTPException の発生
   - エラー時のトレース取得

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
   # 基本的なトレース
   curl http://localhost:8000/hello

   # 非同期計算
   curl http://localhost:8000/async-calc/10/2

   # エラーハンドリング
   curl http://localhost:8000/error-demo
   ```

4. トレースを確認:
   ```bash
   curl http://localhost:8000/eval-track/traces
   ```

詳細な実装については [main.py](./main.py) を参照してください。
