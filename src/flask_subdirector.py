
############################################
# Flask Subdirector - Run Flask in a subdirectory/folder of your main site WITHOUT any change in the code (except call to this function)
#
from werkzeug.middleware.dispatcher import DispatcherMiddleware


__SUBDIR=''
__DEFAULTPAGE=''

# Redirects the root to the subdirectory if ask "www.example.com/" WITHOUT the subdirectory, it will redirect to "www.example.com/subdir/" set earlier
def __simpleRootRedirect(env, resp):
    resp('302 Found', [('Content-Type', 'text/plain'), ('Location', __SUBDIR + '/' + __DEFAULTPAGE)])
    return []


# Makes the Flask app run from a subdirectory like "www.example.com/subdir/"
# Need to pass the app since it's not yet running (no context)
# Subdirectory must be a non-empty string, can be single or multilevel like "a/b/c" 
def run_flask_in_subdirectory(app, subdirectory:str, default_page:str = "home"):
    global __SUBDIR, __DEFAULTPAGE
    # The savior of the day vvv
    #https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes

    sd = subdirectory.strip("/").strip()

    if sd == "":
        raise ValueError("Subdirectory cannot be empty")

    #keep only leading slash
    __SUBDIR = "/" + sd
    __DEFAULTPAGE = default_page.strip("/").strip()

    app.config["APPLICATION_ROOT"] = __SUBDIR

    app.wsgi_app = DispatcherMiddleware(__simpleRootRedirect, {__SUBDIR: app.wsgi_app})