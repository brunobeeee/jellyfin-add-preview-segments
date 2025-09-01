import sqlite3
import uuid

DB_PATH = 'jellyfin.db'
LIBRARY_ID = '<deine-library-id>'


with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    # 1. Alle Item-IDs aus der Library abrufen (ParentId = LIBRARY_ID)
    cursor.execute('''
        SELECT Id 
        FROM Items
        WHERE ParentId = ?
    ''', (LIBRARY_ID,))
    
    item_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"{len(item_ids)} Items in Library gefunden.")
    
    for ITEM_ID in item_ids:
        # 2. Intro-Segment suchen (Typ 5)
        cursor.execute('''
            SELECT StartTicks, EndTicks 
            FROM MediaSegments 
            WHERE ItemId = ? AND Type = 5
        ''', (ITEM_ID,))
        intro_segment = cursor.fetchone()
        
        if not intro_segment:
            print(f"Kein Intro für Item {ITEM_ID}")
            continue
        
        # 3. Preview-Segment prüfen (Typ 6)
        cursor.execute('''
            SELECT 1 FROM MediaSegments WHERE ItemId = ? AND Type = 6
        ''', (ITEM_ID,))
        preview_exists = cursor.fetchone()
        
        if preview_exists:
            print(f"Preview schon vorhanden für Item {ITEM_ID}")
            continue
        
        # 4. Neues Preview-Segment anlegen (0 bis Intro start)
        intro_start, _ = intro_segment
        new_segment_id = str(uuid.uuid4()).upper()
        
        new_segment = (
            new_segment_id,
            intro_start,   # EndTicks (Anfang Intro)
            ITEM_ID,
            'b0338b450421c081992860f1d02f261f',  # SegmentProviderId (z.B. Intro Skipper Plugin)
            0,             # StartTicks (0)
            6              # Type = Preview
        )
        
        cursor.execute('''
            INSERT INTO MediaSegments 
            (Id, EndTicks, ItemId, SegmentProviderId, StartTicks, Type) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', new_segment)
        
        conn.commit()
        
        print(f"Neues Preview-Segment für Item {ITEM_ID} hinzugefügt.")
