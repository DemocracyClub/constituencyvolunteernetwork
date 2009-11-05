from django.db import connection, transaction

def add_login_count():
    cursor = connection.cursor()
    sql = ('ALTER TABLE "signup_customuser" '
    	   'ADD COLUMN "login_count" integer NOT NULL DEFAULT 1; ')
    cursor.execute(sql)

    # everyone who's ever activated their account will
    # for our purposes be considered to have logged in once
    sql = ('UPDATE "signup_customuser" '
           'SET login_count = 2 WHERE user_ptr_id IN '
           ' (SELECT id FROM "auth_user" WHERE '
           '  is_active is True); ')
    cursor.execute(sql)

def add_seen_invite():
    cursor = connection.cursor()
    sql = ('ALTER TABLE "signup_customuser" '
           'ADD COLUMN "seen_invite" boolean NOT NULL DEFAULT False; ')
    cursor.execute(sql)

def main():
    add_login_count()
    transaction.commit_unless_managed()
    add_seen_invite()
    transaction.commit_unless_managed()
    return "done"
