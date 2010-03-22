from hashlib import md5

ynmp_url = "http://stage.yournextmp.com"
YNMP_SECRET = "SECRET_KEY"

def ynmp_login_url(user, task):
    sig = md5("%d%s" % (user.id, YNMP_SECRET)).digest()
    return "%s/democracyclub/login?dc_user_id=%d&name=%s&task=%s&sig=%s" %
                (ynmp_url, user.id, user.display_name, task, sig)
