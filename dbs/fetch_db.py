import sqlite3 as sql

from bot.utils import REALTY_FILEPATH


def update_database(offer: dict) -> bool:
    offer_id = offer['offer_id']

    with sql.connect(REALTY_FILEPATH) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT offer_id FROM offers WHERE offer_id = (?) AND user_id = {offer['user_id']}
        """, (offer_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("""
                INSERT INTO offers
                VALUES (NULL,
                :title, :url, :offer_id, :date, :price, :adress, :area, :rooms, :floor, :total_floor, :location_link, :user_id)
            """, offer)
            connection.commit()
            return True
        return False
