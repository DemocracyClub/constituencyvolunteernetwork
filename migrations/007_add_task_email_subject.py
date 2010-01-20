from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ("""alter table tasks_task add column \"email_subject\"
    VARCHAR(80) NOT NULL DEFAULT 'Task from Democracy Club'""")
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

