# celery_config.py

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine  # Import create_engine from SQLAlchemy
import pandas as pd  # Import pandas

celery = Celery(__name__, broker='http://127.0.0.1:5000')  # Use your Redis broker URL

def update_excel():
    # Connect to the database
    engine = create_engine('sqlite:///sqlalchemy.sqlite')

    # Query the database to fetch new data
    query = "SELECT * FROM Feedback WHERE timestamp > last_update_timestamp"
    df = pd.read_sql_query(query, engine)

    # Export the DataFrame to an Excel file
    excel_file = "feedback_data.xlsx"
    df.to_excel(excel_file, index=False, engine="openpyxl")

@celery.task
def scheduled_update():
    update_excel()

celery.conf.beat_schedule = {
    'update-excel': {
        'task': 'scheduled_update',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}
