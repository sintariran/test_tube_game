# 試験管パズルゲーム

Pythonで実装された試験管パズルゲームです。同じ図形と色の組み合わせを1つの試験管にまとめることが目標です。

## 必要条件

- Python 3.8以上
- pygame
- numpy

## インストール方法

1. リポジトリをクローンまたはダウンロードします
2. 必要なパッケージをインストールします：
   ```bash
   pip install -r requirements.txt
   ```

## 実行方法

以下のコマンドでゲームを起動します：

```bash
python -m src
```

## 遊び方

- マウスクリックで試験管を選択します
- 1つ目のクリックで移動元の試験管を選択
- 2つ目のクリックで移動先の試験管を選択
- 'R'キーでゲームをリセット
- 同じ図形と色の組み合わせを1つの試験管に集めるとクリア！