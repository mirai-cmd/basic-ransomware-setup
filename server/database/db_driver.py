import sqlite3,traceback,dotenv,os
from sqlite3 import ProgrammingError, InternalError, DataError, OperationalError

dotenv.load_dotenv()
def db_get_connection():
    connection = sqlite3.connect(os.getenv('SQLITE_CONNECT_URL'))
    return connection
    
def db_error_handler(exc_type):
    error=""
    if isinstance(exc_type,ProgrammingError):
        error+="ProgrammingError\n"
    elif isinstance(exc_type,DataError):
        error+="DataError\n"
    elif isinstance(exc_type,OperationalError):
        error+="OperationalError\n"
    elif isinstance(exc_type,InternalError):
        error+="InternalError\n"
    else:
        error+="An unexpected error occurred, try restarting the db/server or try again in some time"
    return error+traceback.format_exc()