from django.db import connection, transaction

def main():
    cursor = connection.cursor()
    sql = ('create unique index name_year_idx on signup_constituency (name, year)')
    cursor.execute(sql)

    transaction.commit_unless_managed()

    return "done"

