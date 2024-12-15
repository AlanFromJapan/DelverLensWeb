
##########################################################################
## Lib handling the additional functions like fetching visuals, etc. from external sources
##
## Main API: https://scryfall.com/docs/api/cards/arena
#
import requests
import json
import time
import logging
import functools

cache_ArenaID2ImageURL = {}
BLANK_TILE = "Nothing"

#return the URI from a Scryfall ID of a card and in a supported size by scryfall
@functools.lru_cache(maxsize=2048)
def getImageURLFromScryfallID (scryfall_id, size):
    global cache_ArenaID2ImageURL

    #check the cache first
    if scryfall_id in cache_ArenaID2ImageURL:        
        return cache_ArenaID2ImageURL[scryfall_id]

    #not in cache
    try:
        resp = requests.get("https://api.scryfall.com/cards/%s" % (scryfall_id))
        #Scryfall asked to not flood their service
        time.sleep(0.1)

        if resp.ok:
            j = json.loads(resp.text)
            if "image_uris" in j:
                #single face card
                cache_ArenaID2ImageURL[scryfall_id] = j["image_uris"][size]
            else:
                #multi face cards
                cache_ArenaID2ImageURL[scryfall_id] = j["card_faces"][0]["image_uris"][size]
            return cache_ArenaID2ImageURL[scryfall_id]
        else:
            return BLANK_TILE 
    except:
        logging.error ("WARN: couldn't get tile URL for Scryfall ID %s" % (scryfall_id))

        return BLANK_TILE

