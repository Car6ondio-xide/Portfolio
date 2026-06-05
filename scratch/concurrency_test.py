import asyncio
import httpx

# リクエストを送信するAPIのURL（チケットID: 2 Python超入門ハンズオン を狙います）
URL = "http://127.0.0.1:8000/tickets/purchase"
PAYLOAD = {"ticket_id": 2}

async def send_purchase_request(user_id: int):
    """サーバーへ購入リクエストを送信する関数"""
    async with httpx.AsyncClient() as client:
        try:
            print(f"[User {user_id}] 購入リクエストを送信します...")
            response = await client.post(URL, json=PAYLOAD, timeout=10.0)
            print(f"[User {user_id}] ステータスコード: {response.status_code}")
            print(f"[User {user_id}] レスポンス: {response.json()}")
        except Exception as e:
            print(f"[User {user_id}] エラーが発生しました: {e}")

async def main():
    # ほぼ同時に2つのリクエストを送信するタスクを作成
    task1 = send_purchase_request(1)
    task2 = send_purchase_request(2)
    
    # 2つのタスクを同時に実行開始する
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())
