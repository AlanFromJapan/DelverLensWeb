from flask_subdirector import run_flask_in_subdirectory
import logging

myconfig = {
    "max pokemon id": 150,
    "language" : "fr",

    "gameA cards" : 5,

    "session secret key" : "you can really put whatever you want, it's just to encrypt the thingy!",

    #Normally this should be True, but in case you use this where someone misconfigured the CA check settings then make this False.
    "SSL_CHECK" : True,

    #if true, will print some stats about the cache etc.
    "Show stats" : False,

    "BehindProxy" : False,

    #Block, Cursive or mix
    "letterstyle" : "block",

    #uppercase or lowercase
    "lettercase" : "lowercase",

    #VoiceRSS key for speech to text
    "VoiceRSS key" : "your key here",

    #where is the logfile
    "logfile" : "/tmp/poke-trainer.log",

    #log level
    "loglevel" : logging.INFO,

    #TCP port number to listen to
    "port" : 56788,

    #if you want to run behind a proxy AND in a subdirectory.
    # subdirectory: the name of the subdirectory you want to run the app in. Can be "xxx" or "xxx/yyy" or "xxx/yyy/zzz" etc.
    # default_page: the name of the landing page (default "home")
    "subdirectory" : lambda ap: run_flask_in_subdirectory (ap, "subdir"),
    
}