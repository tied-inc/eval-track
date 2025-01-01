# eval-track ドキュメント

`eval-track` は LLM-ML の可観測性とトラッキングサービスを提供するライブラリです。このドキュメントでは、主要なコンポーネントの使い方と機能について説明します。

## 主要コンポーネント

### [Client](client.md)
トレースデータの取得と保存を行うクライアントクラス。

### [Tracer](tracer.md)
関数やコルーチンの応答をキャプチャするデコレーター。

### [Router](router.md)
トレースデータの API エンドポイント。

## インストール方法

```bash
uv pip install "git+https://github.com/tied-inc/eval-track/tracker"
```

詳細な使用方法は各コンポーネントのドキュメントを参照してください。
