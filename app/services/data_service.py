import pandas as pd
from dotenv import load_dotenv
from fastapi.logger import logger
from ..config.logger_config import get_logger
from sqlalchemy import text

load_dotenv()


def load_data(db_obj,filepath):

    df=pd.read_csv(filepath)
    db_obj.insert_data(df,'test','rap_etl')
    unique_values = list(df['ResponseID'].unique())


    for response_id in unique_values:
        db_obj.execute_query(text(f"EXEC update_rap_tables @ResponseID = '{response_id}';"))

    return True