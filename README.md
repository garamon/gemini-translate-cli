# Gemini Translation

Google Gemini API を使用してテキストや Web ページを翻訳する CLI ツール

## 概要

`gemini-translate`は、テキストや Web ページの URL を受け取り、Google Gemini API を使用して指定された言語に翻訳するコマンドラインツールです。
macOS の`pbpaste`コマンドと組み合わせることで、クリップボードの内容を簡単に翻訳できます。

### 主な機能

- 標準入力からのテキスト翻訳
- Web ページの URL 翻訳（メインコンテンツを自動抽出）
- 多言語対応（デフォルト：日本語）
- 複数の Gemini モデルに対応

## 必要条件

- Python 3.13 以上
- Google Gemini API キー
- uv パッケージマネージャー（[インストール方法](https://github.com/astral-sh/uv)）

## インストール

### グローバルインストール（推奨）

```bash
git clone https://github.com/garamon/gemini-translate-cli.git
cd gemini-translate-cli

# グローバルツールとしてインストール
uv tool install .
```

### 開発用インストール

開発やカスタマイズを行う場合：

```bash
# 依存関係のインストール
uv sync

# または開発モードでインストール
uv pip install -e .
```

## 環境変数の設定

### 必須設定

Gemini API キーを取得し、環境変数に設定：

```bash
export GTR_API_KEY='your-api-key-here'
```

### オプション設定

デフォルトでは`gemini-2.5-pro`が使用されますが、環境変数で変更可能です：

```bash
# Gemini 2.5 Flash を使用（高速な翻訳）
export GTR_MODEL='gemini-2.5-flash'
```

永続的に設定する場合は、`.bashrc`、`.zshrc`などのシェル設定ファイルに追加してください：

```bash
# ~/.bashrc または ~/.zshrc に追加
export GTR_API_KEY='your-api-key-here'
export GTR_MODEL='gemini-2.5-pro'
```

## 使用方法

### 基本的な使用方法

#### テキストの翻訳

```bash
# クリップボードの内容を日本語に翻訳（macOS）
pbpaste | gtr

# ファイルの内容を翻訳
cat document.txt | gtr

# 直接テキストを入力して翻訳
echo "Hello, world!" | gtr
```

#### Web ページの翻訳

```bash
# URLを指定してWebページを翻訳
gtr https://example.com/article.html

# 特定の言語に翻訳
gtr https://example.com -t Spanish
```

### 翻訳先言語の指定

デフォルトでは日本語に翻訳されますが、`-t`オプションで他の言語を指定できます：

```bash
# 英語に翻訳
pbpaste | gtr -t English

# スペイン語に翻訳
echo "こんにちは" | gtr -t Spanish

# フランス語に翻訳
cat input.txt | gtr --target French
```

### ヘルプ

```bash
gtr --help
```

## 開発

### リンターの実行

```bash
just lint
# または
uv run ruff check --fix .
```

### コードフォーマット

```bash
just format
# または
uv run ruff format .
```
