from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLiteのデータベースファイルパスを指定（プロジェクト直下に tickets.db というファイルが作られます）
SQLALCHEMY_DATABASE_URL = "sqlite:///./tickets.db"

# データベースエンジンを作成
# connect_args={"check_same_thread": False} はSQLite特有の設定で、
# FastAPIのようなマルチスレッドのWebアプリで安全に動作させるために必要です
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

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
