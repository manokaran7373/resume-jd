import json
import os
import mysql.connector
from logger import Logger
from dotenv import load_dotenv

load_dotenv()

class JobDescriptionDB:
    def __init__(self):
        self.logger = Logger("database")
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
            )
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info("Database connection established successfully")
        except mysql.connector.Error as err:
            self.logger.error(f"Database connection failed: {err}")
            raise

    def get_all_job_descriptions(self):
        try:
            query = "SELECT id, `key`, `value` FROM job_desc_content"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            job_descriptions = {}

            for row in results:
                job_id = row["id"]  # Ensure unique ID
                job_descriptions[job_id] = json.loads(
                    row["value"]
                )  # Store with ID instead of key

            return job_descriptions

        except Exception as e:
            self.logger.error(f"Error retrieving job descriptions: {e}")
            raise

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            self.logger.info("Database connection closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing database connection: {e}")
