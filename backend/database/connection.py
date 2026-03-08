import psycopg2


def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ai_mock_interview",
        user="postgres",
        password="postgres123",
        port="5432"
    )
    return conn