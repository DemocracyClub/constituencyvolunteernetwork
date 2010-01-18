from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ('alter table tasks_badge add column "number" int DEFAULT 1 NOT NULL')
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

