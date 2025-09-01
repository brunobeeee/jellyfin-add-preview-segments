import sqlite3
import uuid
import os

from dotenv import load_dotenv

from get_episode_ids import get_episode_ids

load_dotenv()
jellyfin_url = os.getenv("Jellyfin_URL")
api_key = os.getenv("API_Key")
library_id = os.getenv("Library_ID")
db_path = os.getenv("DB_Path")

episodes = get_episode_ids(jellyfin_url, api_key, library_id)

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Select all rows from db where ItemId is in the list of episodes from the library
    episodes_tuple = tuple(episodes) # Convert list to tuple for SQL query
    cursor.execute(f"""
        SELECT ms_intro.ItemId, ms_intro.StartTicks
        FROM MediaSegments ms_intro
        WHERE ms_intro.Type = 5
        AND ms_intro.StartTicks != 0
        AND ms_intro.ItemId IN ({','.join(['?']*len(episodes))})
        AND NOT EXISTS (
            SELECT 1 FROM MediaSegments ms_preview
            WHERE ms_preview.ItemId = ms_intro.ItemId
            AND ms_preview.Type = 2
        )
    """, episodes_tuple)
    intros = cursor.fetchall()
    print(f"Found {len(intros)} intros without preview segments.")

    # For every entry add a new row with same ItemId, new UUID, StartTicks=0 and EndTicks=StartTicks_of_intro
    for intro in intros:
        item_id = intro[0]
        end_ticks = intro[1]
        new_id = str(uuid.uuid4()).upper()
        cursor.execute("INSERT INTO MediaSegments (Id, EndTicks, ItemId, SegmentProviderId, StartTicks, Type) VALUES (?, ?, ?, 'b0338b450421c081992860f1d02f261f', 0, 2)", (new_id, end_ticks, item_id))
        print(f"Inserted intro skip segment for item {item_id} with new id {new_id}")
    conn.commit()

print("Done.")