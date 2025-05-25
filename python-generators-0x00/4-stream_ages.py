import seed

def stream_user_ages():
    """
    Fetches user ages one by one from the user_data table using a generator.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT age FROM user_data")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row[0]
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    user_count = 0
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")

if __name__ == '__main__':
    calculate_average_age()