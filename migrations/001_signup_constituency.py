from django.db import connection, transaction
from signup.management.commands.constituencies import Command

def add_new_columns():
    cursor = connection.cursor()
    sql = ('ALTER TABLE "signup_constituency" '
    	   'ADD COLUMN "lat" double precision; '
	   'ALTER TABLE "signup_constituency" '
	   'ADD COLUMN "lon" double precision;')
    cursor.execute(sql)

def main():
    add_new_columns()
    transaction.commit_unless_managed()
    c = Command()
    c.handle('update')
    return "done"
