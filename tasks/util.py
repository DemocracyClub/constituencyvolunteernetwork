from django.core.urlresolvers import reverse
from signup.views import do_login

def login_key(func):
    """
        Generate code to handle login_key based login. Allows use of other decorators
        such as @login_required
    """
    def new_func(*args, **kwargs):
        if 'login_key' in kwargs:
            login_key = kwargs['login_key']
            request = args[0]
        
            if login_key is not None:
                # should we generate separate login keys for each taskuser for security?
                do_login(request, login_key)
        
            del kwargs['login_key']

        return func(*args, **kwargs)
    return new_func

def reverse_login_key(name, user, args=None, kwargs=None):
    """
        Sort out the login key for a reverse call
    """
    if args is None: args = []
    if kwargs is None: kwargs = {}
    
    key = user.registrationprofile_set.get().activation_key
    kwargs['login_key'] = key

    return reverse(name, args=args, kwargs=kwargs)

