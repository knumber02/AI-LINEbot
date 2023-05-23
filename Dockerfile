# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー
COPY pyproject.toml poetry.lock ./

# poetryでライブラリをインストール
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# openai moduleを明示的にインストール
RUN poetry add openai

# uvicornのサーバーを立ち上げる
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
