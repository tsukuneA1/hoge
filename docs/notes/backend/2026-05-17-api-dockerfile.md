<!-- ```Dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*
```
Ubuntu/Devian系のパッケージ一覧を更新し、build-essential(C/C++のビルドに必要な基本ツール一式),g++(C++コンパイラ)をインストールしたのち、apt-get updateで取得したパッケージ一覧のキャッシュを削除 -->

```Dockerfile
RUN groupadd -g 1000 app && useradd -r -u 1000 -g app -m app && \
    mkdir -p /home/app/.cache/uv && \
    chown -R app:app /app /home/app/.cache
USER app
```
groupID1000のグループを作成する。
次にsystem userとして(-r), UIDを1000で(-u 1000)、appグループで(-g app)、ホームディレクトリに(-m)、ユーザーをappとして作る(app) (home/app)
uv用のキャッシュディレクトリを作っている
/appと/home/app/.cacheの所有権をappユーザー・appグループに変更している。
-Rはディレクトリの中身もまとめて変更する
USER appでこれ以降rootユーザーではなくappで実行する。

```Dockerfile
COPY --chown=app:app pyproject.toml uv.lock ./
COPY --chown=app:app packages/ /app/packages/
```
ホスト側のファイルをDockerイメージ内にコピーしつつ、コピー後の所有権をapp:appにする。

```Dockerfile
RUN --mount=type=cache,target=/home/app/.cache/uv,uid=1000,gid=1000 \
    uv sync --frozen --no-dev --no-editable --package api
```

uvのキャッシュをappユーザーで使えるようにマウントし(--mount=type=cache, target=/home/app/.cache/uv, uid=1000, gid=1000 \)、uv.lockに従って本番用の依存関係を/app/.venvにインストールしている(uv sync --frozen --no-dev --no-editable --package api)。

```Dockerfile
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

RUN groupadd -g 1000 app && useradd -r -u 1000 -g app -m app && \
    chown app:app /app
USER app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 

CMD ["uvicorn", "api:main:app"]
```
新しい FROM で WORKDIR / USER / ENV などはリセットされる
だから実行用ステージでも WORKDIR と app ユーザーを作り直している

builder ステージで作った /app/.venv だけをコピーしている
PATH に /app/.venv/bin を追加している
CMD で venv 内の uvicorn を使って FastAPI アプリを起動している