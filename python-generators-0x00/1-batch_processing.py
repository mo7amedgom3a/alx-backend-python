import seed

def stream_users_in_batches(batch_size):
    """
    Fetches rows from the user_data table in batches using a generator.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM user_data")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user[3] > 25]
        yield filtered_users
