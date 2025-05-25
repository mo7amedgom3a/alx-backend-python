import seed

def stream_users():
    """
    Fetches rows one by one from the user_data table using a generator.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM user_data")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()
            connection.close()