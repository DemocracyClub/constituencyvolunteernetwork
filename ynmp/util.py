from hashlib import md5
from settings import YNMP_SECRET_KEY, YNMP_URL

def ynmp_login_url(user, task):
    sig = md5("%d%s" % (user.id, YNMP_SECRET_KEY)).hexdigest()
    return "%sauth/dc_login?dc_user_id=%d&name=%s&task=%s&sig=%s" % \
                (YNMP_URL, user.id, user.display_name, task, sig)

