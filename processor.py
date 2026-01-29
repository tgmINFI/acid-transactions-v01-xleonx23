import sqlite3

class ShipmentProcessor:
    def __init__(self, db_path):
        self.db_path = db_path

    def process_shipment(self, item_name, quantity, log_callback):
        """
        Executes the shipment logic using ACID principles.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        log_callback(f"--- STARTING TRANSACTION: Move {quantity} of {item_name} ---")

        try:
            # Wir starten einen Block, der beide Operationen umschließt.
            # SQLite startet implizit eine Transaktion beim ersten EXECUTE.

            # STEP 1: Update Inventory
            cursor.execute("UPDATE inventory SET stock_qty = stock_qty - ? WHERE item_name = ?", 
                           (quantity, item_name))
            
            # Falls die Inventory-Einschränkung (CHECK constraint) verletzt wird, 
            # wirft SQLite hier eine IntegrityError.
            log_callback(">> STEP 1 SUCCESS: Inventory Deducted.")

            # STEP 2: Log the Shipment
            cursor.execute("INSERT INTO shipment_log (item_name, qty_moved) VALUES (?, ?)", 
                           (item_name, quantity))
            log_callback(">> STEP 2 SUCCESS: Shipment Logged.")

            # Wenn wir hier ankommen, war ALLES erfolgreich.
            conn.commit()
            log_callback("--- TRANSACTION COMMITTED SUCCESSFULLY ---")

        except Exception as e:
            # Falls IRGENDETWAS schiefgeht (Schritt 1 ODER Schritt 2), 
            # machen wir alles rückgängig.
            conn.rollback()
            log_callback(f">> TRANSACTION FAILED: {e}")
            log_callback("--- ROLLBACK EXECUTED: No changes were made to the database. ---")

        finally:
            # Die Verbindung muss immer geschlossen werden.
            conn.close()