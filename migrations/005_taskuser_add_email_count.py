from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ('alter table tasks_taskuser add column "emails_sent" int DEFAULT 0')
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

