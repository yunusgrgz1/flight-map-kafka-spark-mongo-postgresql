import os
import psycopg2
import logging
import pandas as pd

OUTPUT_DIR = "/opt/airflow/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("DailyReportGenerator")

# PostgreSQL connection function
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

# Query 1: Delayed Status Distribution
def get_delayed_status_distribution(cursor):
    query = """
        SELECT delayed_status, COUNT(*) 
        FROM flights
        GROUP BY delayed_status
        ORDER BY COUNT(*) DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Query 2: Top 5 Airlines with Most Flights
def get_top_5_airlines(cursor):
    query = """
        SELECT airline, COUNT(*) 
        FROM flights
        GROUP BY airline
        ORDER BY COUNT(*) DESC
        LIMIT 5;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Query 3: Top 10 Airlines with Highest "Too Delayed" / Delayed Status Ratio
def get_top_10_airlines_by_delay_ratio(cursor):
    query = """
        SELECT airline, 
               COUNT(CASE WHEN delayed_status = 'too_late' THEN 1 END) * 1.0 / COUNT(delayed_status) AS delay_ratio
        FROM flights
        GROUP BY airline
        ORDER BY delay_ratio DESC
        LIMIT 10;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Function to write data to CSV file

def write_to_csv(filename, data):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"Data written to {filename} successfully using pandas.")
    except Exception as e:
        logger.error(f"Failed to write data to {filename}: {e}")

# Main function to generate the daily report
def generate_daily_report():
    try:
        logger.info("Starting the daily report generation...")
        cursor, conn = postgres_connection()

        # Query 1: Delayed Status Distribution
        delayed_status_data = get_delayed_status_distribution(cursor)
        write_to_csv(os.path.join(OUTPUT_DIR, "delayed_status_distribution.csv"), delayed_status_data)

        # Query 2: Top 5 Airlines with Most Flights
        top_5_airlines_data = get_top_5_airlines(cursor)
        write_to_csv(os.path.join(OUTPUT_DIR, "top_5_airlines.csv"), top_5_airlines_data)

        # Query 3: Top 10 Airlines with Highest "Too Delayed" / Delayed Status Ratio
        top_10_airlines_by_delay_ratio_data = get_top_10_airlines_by_delay_ratio(cursor)
        write_to_csv(os.path.join(OUTPUT_DIR, "top_10_late_ratio_airlines.csv"),top_10_airlines_by_delay_ratio_data )

        conn.close()
        logger.info("Daily report generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate daily report: {e}")

# Entry point
if __name__ == "__main__":
    generate_daily_report()
