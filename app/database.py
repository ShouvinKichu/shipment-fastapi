import sqlite3
from typing import Any
from app.schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)"
        )

    
    def create(self, shipment: ShipmentCreate) -> int:
        self.cursor.execute("SELECT MAX(id) fROM shipment")
        result = self.cursor.fetchone()

        new_id = (result[0] or 12700) + 1
        self.cursor.execute("""
            INSERT INTO shipment VALUES(:id, :content, :weight, :status)
        """,
            {
                "id" : new_id,
                **shipment.model_dump(),
                "status" : "Placed",
            }
        )          
        self.connection.commit()
        return new_id
    
    def get_latest(self) -> dict[str, Any] | None:
        self.cursor.execute("SELECT * FROM shipment ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result is None:
            return None
        return {
            "id": result[0],
            "content": result[1],
            "weight": result[2],
            "status": result[3],
        }


    def get(self, id : int) -> dict[str, Any] | None:
        self.cursor.execute("""
            SELECT * FROM shipment WHERE id = ?
        """, (id,))
        result = self.cursor.fetchone()
        return {
            "id" : result[0],
            "content" : result[1],
            "weight" : result[2],
            "status" : result[3],
        } if result else None

    
    def update(self,id: int, shipment : ShipmentUpdate) -> dict[str, Any] | None:
        self.cursor.execute("""
            UPDATE shipment SET status = :status 
            WHERE id = :id
        """, 
            {
                "id" : id, 
                **shipment.model_dump(),
            }
        )
        self.connection.commit()
        return self.get(id)
    
    
    def delete(self, id : int):
        self.cursor.execute("""
            DELETE FROM shipment WHERE id = ?
        """,(id,))
        self.connection.commit()


    def close(self):
        self.connection.close()

