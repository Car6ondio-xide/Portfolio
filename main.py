from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import redis

r = redis.Redis(host="localhost", port = 6379, db = 0, decode_responses = True)

# データベースのテーブルを作成（存在しない場合のみ作成されます）
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQLite Ticket API")

# テスト用の初期データを登録する関数
def seed_data():
    db = next(get_db())
    # チケットテーブルが空の場合のみ、初期データを投入する
    if db.query(models.Ticket).count() == 0:
        initial_tickets = [
            models.Ticket(name="メガベンチャーキャリアカンファレンス 2026", stock=5),
            models.Ticket(name="Python超入門ハンズオン", stock=2),
            models.Ticket(name="インフラエンジニア交流会", stock=0),
        ]
        db.add_all(initial_tickets)
        db.commit()
    db.close()

# アプリ起動時に初期データを投入
seed_data()

# リクエストデータのバリデーション定義
class PurchaseRequest(BaseModel):
    ticket_id: int

@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    """データベースからチケット一覧と在庫状況を取得します"""
    # SELECT * FROM tickets; を実行するのと同等
    tickets = db.query(models.Ticket).all()
    return tickets

@app.post("/tickets/purchase")
def purchase_ticket(request: PurchaseRequest, db: Session = Depends(get_db)):
    """データベースからチケットを購入し、在庫を減らします"""
    # 1. データベースから指定されたIDのチケットを検索
    # SELECT * FROM tickets WHERE id = ticket_id LIMIT 1;
    ticket = db.query(models.Ticket).filter(models.Ticket.id == request.ticket_id).with_for_update().first()

    if not ticket:
        raise HTTPException(status_code=404, detail="指定されたチケットが見つかりません。")

    # 2. 在庫を確認
    if ticket.stock <= 0:
        raise HTTPException(status_code=400, detail="申し訳ありません。チケットは売り切れました。")

    # 3. 在庫を減らしてデータベースに保存（コミット）
    ticket.stock -= 1
    db.commit()      # 変更内容を確定して保存
    db.refresh(ticket) # 最新の状態にデータを更新

    key = "limit:purchase"
    current_requests = r.get(key)

    if current_requests and int(current_requests) >= 3:
        raise HTTPException(
                status_code = 429,
                detail = "リクエストが多すぎます。しばらく時間を置いてから再度お試しください。"
                )

    if not current_requests:
        r.set(key, 1, ex=10)
    else:
        r.incr(key)

    ticket = db.query(models.Ticket).filter(models.Ticket.id == request.ticket_id).with_for_update().first()

    return {
        "message": "チケットの購入が完了しました！(SQLite)",
        "ticket_name": ticket.name,
        "remaining_stock": ticket.stock
    }

