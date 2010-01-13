from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ('alter table tasks_badge add column "date_awarded" timestamp with time zone NOT NULL')
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

