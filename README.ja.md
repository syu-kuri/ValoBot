# Valobot

Valorantカスタム対戦管理のためのDiscord Botです。discord.py Components v2を使ったキュー管理とチーム分け機能を提供します。

[English version](README.md)

---

## 機能

- `/recruit` — 参加者募集を開始し、リアルタイムで更新されるEmbedを表示
- **Join / Leave** — ボタン操作でキューへの参加・離脱が可能
- **Split Teams** — キュー内のプレイヤーをランダムに2チームへ振り分け
- **Reset** — 管理者はいつでもキューをリセット可能
- `/map-roulette` — スプラッシュ画像付きでVALORANTのマップをランダム抽選（スタンダード / スカーミッシュ / TDM対応）

---

## 動作要件

- Python 3.12以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- Discord Botトークン（[Discord Developer Portal](https://discord.com/developers/applications) で取得）

---

## セットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/syu-kuri/valobot.git
cd valobot

# 2. 依存パッケージをインストール
uv sync

# 3. 環境変数を設定
cp .env.sample .env
# .env を編集して DISCORD_TOKEN を設定する

# 4. マップ画像をダウンロード（/map-roulette に必要）
uv run python scripts/download_maps.py

# 5. Botを起動
uv run python main.py
```

---

## ISSUEの送り方

1. [既存のISSUE](../../issues) を検索して重複がないか確認してください。
2. **New Issue** をクリックし、適切なテンプレートを選択してください。
   - **Bug Report（バグ報告）** — 不具合や予期しない動作が発生している場合。
   - **Feature Request（機能リクエスト）** — 新機能や改善のアイデアがある場合。
3. 必須項目をすべて記入して送信してください。

> 一般的な質問は、ISSUEではなく [GitHub Discussions](../../discussions) をご利用ください。

---

## コントリビュート

フォークワークフロー・ブランチ命名規則・コード規約・PR手順の詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## マップ画像について

マップのスプラッシュ画像はRiot Gamesの著作物のため、このリポジトリには含まれていません。
クローン後に `scripts/download_maps.py` を実行すると、[valorant-api.com](https://valorant-api.com) から自動でダウンロードできます。
画像はDiscord上での表示のみに使用し、再配布は行いません。

> 全てのゲームアセットはRiot Gamesに帰属します。本プロジェクトはRiot Gamesとは無関係であり、公式の承認を受けたものではありません。

---

## マップ画像について

マップのスプラッシュ画像はRiot Gamesの著作物のため、このリポジトリには含まれていません。
クローン後に `scripts/download_maps.py` を実行すると、[valorant-api.com](https://valorant-api.com) から自動でダウンロードできます。
画像はDiscord上での表示のみに使用し、再配布は行いません。

> 全てのゲームアセットはRiot Gamesに帰属します。本プロジェクトはRiot Gamesとは無関係であり、公式の承認を受けたものではありません。

---

## ライセンス

[MIT](LICENSE)
