from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ("""alter table issue_issue alter column \"reference_url\"
    type VARCHAR(2048)""")
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

