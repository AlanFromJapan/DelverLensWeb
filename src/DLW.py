import logging
import os
import requests
import random
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, current_app, session, request, make_response
#running behind proxy?                                                                                            
from werkzeug.middleware.proxy_fix import ProxyFix

from config import myconfig
import dbutils
import scryfall

########################################################################################
## Flask vars
#
app = Flask(__name__, static_url_path='')
app.secret_key = myconfig["session secret key"]

#if behind a proxy set the WSGI properly 
# see http://electrogeek.tokyo/setup%20flask%20behind%20nginx%20proxy.html
if myconfig.get("BehindProxy", False):
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'])

########################################################################################
## Other non-web related functions
#
#-----------------------------------------------------------------------
#Indirection so I can keep the API key on server side (useless, but I don't want to expose it)
@app.route("/api/text2speech/<lang>/<message>", methods=['GET'])
def text_to_speech(lang, message):
    logging.info(f"S2T: {lang} - '{message}'")
    
    #The API expects a specific locale "fr-fr", "ja-jp", "ko-kr" and not just a language code on 2 letters
    locale =  "fr-fr" if lang == "fr" else "ja-jp" if lang == "jp" else "ko-kr"

    try:
        speed_factor = myconfig.get("VoiceRSS speed", 0)
        url = f"https://api.voicerss.org/?key={myconfig['VoiceRSS key']}&hl={locale}&c=MP3&v=Zola&f=16khz_16bit_mono&r={speed_factor}&src={message}"
        logging.debug(f"URL for S2T: {url}")
        req = requests.Request('GET', url)
        prepared = req.prepare()
        resp = requests.Session().send(prepared, stream=True, verify=myconfig["SSL_CHECK"])
    
        return resp.raw.read(), resp.status_code, resp.headers.items()
    except Exception as e:
        logging.error(f"Error in text_to_speech: {str(e)}")
        return None, 500, None

########################################################################################
## Web related functions
#
#-----------------------------------------------------------------------
#Landing page, not much to see here but at least if API connectivity doesn't you will know immediately


@app.route('/')
@app.route('/home')
def homepage():
    imgs = []

    all_cards = dbutils.getAllCards()

    all_collections = dbutils.getAllCollections()

    if len(all_collections) > 0:
        collection = dbutils.getCollectionCards(all_collections[0])
        for i in range(10):
            if i >= len(collection.card_ids):
                break
            card = all_cards[collection.card_ids[i]]
            card.image = scryfall.getImageURLFromScryfallID(card.scryfall_id, "normal")
            imgs.append(all_cards[collection.card_ids[i]].image)

    return render_template("home01.html", pagename="Home", imgs=imgs, **current_app.global_render_template_params)


@app.before_request
def set_global_variables():
    current_app.global_render_template_params = {} 


@app.route("/help")
def help_page():
    return render_template("help01.html", pagename="Help", **current_app.global_render_template_params)

########################################################################################
## Main entry point
#
if __name__ == '__main__':
    try:
        #logging
        directory = os.path.dirname(myconfig.get("logfile", "/tmp/dlw.log"))
        if directory != "" and not os.path.exists(directory):
            os.makedirs(directory)

        logging.basicConfig(filename=myconfig.get("logfile", "/tmp/dlw.log"), level=myconfig.get("loglevel", logging.INFO))

        app.logger.warning("Starting the app")

        #init the database
        dbutils.init()

        #start web interface
        app.debug = True
        app.run(host='0.0.0.0', port=myconfig.get("port", 12345), threaded=True)

    except Exception as e:
        print("Error in main: %s" % str(e))
        app.logger.error("Error in main: %s" % str(e))
        raise