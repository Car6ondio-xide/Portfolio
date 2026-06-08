from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .envファイルからパスワードなどの設定をを読み込む
load_dotenv()

# .envにあるDATABASE_URLを取得し、なければデフォルト値を使用します
SQLALCHEMY_DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://myuser:mypassword@localhost:5432/ticketdb"
        )

# データベースエンジンの作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)




# データベースを操作するための「セッション」を作るクラス
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースのテーブルを定義するためのベースクラス
Base = declarative_base()

# 各APIリクエストで使うデータベースセッションを準備し、終わったら閉じる関数（依存性注入用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
