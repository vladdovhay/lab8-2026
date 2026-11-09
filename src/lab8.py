import psycopg2
import os

DB_NAME = "hotel"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASSWORD", "123450go")
DB_HOST = "localhost"
DB_PORT = "5432"


def main():
    conn = None
    cur = None
    try:
        # Task 2 - Connect
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connected successfully")
        cur = conn.cursor()

        # Task 3 - Create table
        cur.execute("DROP TABLE IF EXISTS rooms;")
        create_table_query = """
        CREATE TABLE rooms (
            id SERIAL PRIMARY KEY,
            room_number INTEGER NOT NULL,
            room_type VARCHAR(50),
            price_per_night NUMERIC(10, 2)
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'rooms' created successfully.")

        # Task 4 - Insert data
        insert_query = """
        INSERT INTO rooms (room_number, room_type, price_per_night)
        VALUES (%s, %s, %s);
        """
        room_data = [
            (101, "Standard", 800.00),
            (102, "Standard", 850.00),
            (201, "Deluxe", 1500.00),
            (202, "Suite", 2500.00),
            (301, "Economy", 500.00)
        ]
        cur.executemany(insert_query, room_data)
        conn.commit()
        print(f"{cur.rowcount} records inserted successfully.")

        # Task 5 - Update data
        update_query = """
        UPDATE rooms
        SET price_per_night = 900.00
        WHERE room_number = 101;
        """
        cur.execute(update_query)
        conn.commit()
        print(f"{cur.rowcount} record(s) updated successfully.")

        # Task 6 - Delete data (найдешевший номер)
        cur.execute("SELECT MIN(price_per_night) FROM rooms;")
        min_price = cur.fetchone()[0]
        delete_query = "DELETE FROM rooms WHERE price_per_night = %s;"
        cur.execute(delete_query, (min_price,))
        conn.commit()
        print(f"{cur.rowcount} record(s) deleted successfully.")

        # Task 7 - Select data
        select_query = """
        SELECT * FROM rooms
        WHERE room_type LIKE 'S%'
        ORDER BY price_per_night ASC;
        """
        cur.execute(select_query)
        records = cur.fetchall()
        print("\n--- Room Records ---")
        for r in records:
            print(f"ID: {r[0]}, Room number: {r[1]}, Type: {r[2]}, Price per night: {r[3]}")
        print("--------------------\n")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while working with PostgreSQL: {error}")

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()