from config import DB_USER,DB_PASS,DB_HOST,DB_NAME
import mysql.connector

db = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST, database=DB_NAME)
cursor = db.cursor(buffered=True)
# def main():
#     pass

# if __name__ == "__main__":
#      main()
     


