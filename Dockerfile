# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# プロジェクトファイル全体をコピー
COPY . .

# poetryでライブラリをインストール
RUN poetry install --no-root

# uvicornのサーバーを立ち上げる
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
