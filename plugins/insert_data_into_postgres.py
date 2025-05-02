from pymongo import MongoClient
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("KafkaFlightConsumer")

# MongoDB connection
def mongo_connection():
    try:
        logger.info("Connecting to MongoDB...")
        client = MongoClient("mongodb://root:example@mongodb:27017")
        db = client["mydb"]
        collection = db["mycollection"]
        logger.info("Connected to MongoDB successfully.")
        return collection
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

# PostgreSQL connection
def postgres_connection():
    try:
        logger.info("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port="5432")
        cursor = conn.cursor()
        logger.info("Connected to PostgreSQL successfully.")
        return cursor, conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise

# Fetch data from MongoDB
def get_data_from_mongo(collection):
    try:
        logger.info("Fetching data from MongoDB collection...")
        filtered_data = collection.find(
            {
                "actual_landed_time": {"$ne": None}
            },
            {
                "_id": 0,
                "flight_id": 1,
                "airline": 1,
                "flight_status": 1,
                "departure_city": 1,
                "departure_airport": 1,
                "arrival_city": 1,
                "arrival_airport": 1,
                "scheduled_departure_time": 1,
                "actual_departure_time": 1,
                "scheduled_arrival_time": 1,
                "actual_landed_time": 1,
            })

        data_list = list(filtered_data)
        logger.info(f"Fetched {len(data_list)} records from MongoDB.")
        return data_list
    except Exception as e:
        logger.error(f"Error while fetching data from MongoDB: {e}")
        raise



# Insert data into PostgreSQL
def insert_data_into_postgres(cursor, conn, filtered_data):
    try:
        logger.info(f"Inserting {len(filtered_data)} records into PostgreSQL...")
        for doc in filtered_data:
            scheduled_arrival = doc.get("scheduled_arrival_time")
            actual_landed = doc.get("actual_landed_time")

            delayed_status = None
            if scheduled_arrival and actual_landed:
                
                if isinstance(scheduled_arrival, str):
                    scheduled_arrival = datetime.fromisoformat(scheduled_arrival)
                if isinstance(actual_landed, str):
                    actual_landed = datetime.fromisoformat(actual_landed)

                delay_minutes = (actual_landed - scheduled_arrival).total_seconds() / 60

                if delay_minutes < 15:
                    delayed_status = "on_time"
                elif 15 <= delay_minutes < 30:
                    delayed_status = "slightly_delayed"
                else:
                    delayed_status = "too_late"

            cursor.execute("""
                INSERT INTO ucuslar (
                    flight_id,
                    airline,
                    flight_status,
                    departure_city,
                    departure_airport,
                    arrival_city,
                    arrival_airport,
                    scheduled_departure_time,
                    actual_departure_time,
                    scheduled_arrival_time,
                    actual_landed_time,
                    delayed
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                doc.get("flight_id"),
                doc.get("airline"),
                doc.get("flight_status"),
                doc.get("departure_city"),
                doc.get("departure_airport"),
                doc.get("arrival_city"),
                doc.get("arrival_airport"),
                doc.get("scheduled_departure_time"),
                doc.get("actual_departure_time"),
                scheduled_arrival,
                actual_landed,
                delayed_status
            ))

        conn.commit()
        logger.info("Data inserted into PostgreSQL and committed successfully.")
    except Exception as e:
        logger.error(f"Error while inserting data into PostgreSQL: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
        logger.info("PostgreSQL connection closed.")

# Main function to fetch and insert data
def get_and_insert_data():
    try:
        logger.info("Starting data transfer from MongoDB to PostgreSQL.")
        collection = mongo_connection()
        cursor, conn = postgres_connection()
        filtered_data = get_data_from_mongo(collection)
        if filtered_data:
            insert_data_into_postgres(cursor, conn, filtered_data)
        else:
            logger.info("No data to insert into PostgreSQL.")
    except Exception as e:
        logger.error(f"Data transfer failed: {e}")

# Entry point
if __name__ == "__main__":
    get_and_insert_data()
