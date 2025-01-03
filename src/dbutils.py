import sqlite3
import os
from  delverObjects import Collection, Card
import logging

__MASTER_DB_FILTER = "_backup.dlens"
__MASTER = ""

__EXPORTED_DB_FILTER = "_exported.dlens"
__EXPORTS = []

__ALL_CARDS = {}

#attribute all_cards, more elegant
def __getattr__(name):
    if name == 'all_cards':
        return getAllCards()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


#Initiate the database utility
def init(db_file=None):
    global __EXPORTS
    setMasterDB(None)
    __EXPORTS = findExportedDBs()


#finds ONE master database in the input/ folder
def findMasterDB():
    input_folder = os.path.join(os.path.dirname(__file__), 'input')
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(__MASTER_DB_FILTER):
            return os.path.join(input_folder, file_name)
    return None


#finds ALL the exported databases in the input/ folder
def findExportedDBs():
    input_folder = os.path.join(os.path.dirname(__file__), 'input')
    exported_dbs = []
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(__EXPORTED_DB_FILTER):
            exported_dbs.append(os.path.join(input_folder, file_name))
    return exported_dbs


#sets master database (or finds one if None)
def setMasterDB(master: None):
    global __MASTER
    if master is None:
        __MASTER = findMasterDB()
    else:
        __MASTER = master


#returns ALL the cards in the master database
def getAllCards():
    global __MASTER, __ALL_CARDS
    if not __MASTER:
        raise ValueError("Master database is not set.")

    if __ALL_CARDS:
        return __ALL_CARDS
    
    logging.info("getAllCards() - Loading all cards from the master database")

    conn = sqlite3.connect(__MASTER)

    try:
        cursor = conn.cursor()
        
        #beware: table data_cards joins to [data_names._id] on the [data_cards.name] field NOT [data_cards._id] because of ALTERNATE versions of the card
        #so group by to get 1 answer per card, Min(scryfall_id) to get the first scryfall_id found
        cursor.execute("""
SELECT 
    names._id, names.name, names.mana, names.type, names.rules, names.rulings, MIN(cards.scryfall_id) as scryfall_id  
FROM 
    data_names as names join data_cards as cards ON names._id = cards.name
GROUP BY 
    names._id, names.name, names.mana, names.type, names.rules, names.rulings
                       """)
        rows = cursor.fetchall()
    finally:    
        conn.close()
    
    __ALL_CARDS = {}
    for row in rows:
        c = Card(id = int(row[0]), name=row[1], mana=row[2], type=row[3], description=row[4], ruling=row[5], scryfall_id= row[6])
        __ALL_CARDS[c.id] = c
    
    return __ALL_CARDS
    

#updates a collection ALL the cards IDs from the exported databases
def getCollectionCards(c : Collection):
    if not __EXPORTS:
        raise ValueError("No exported databases found.")

    collection_cards = []

    for db in __EXPORTS:
        conn = sqlite3.connect(db)
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT cards._id FROM cards WHERE cards.list = ?", (c.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        
        for row in rows:
            collection_cards.append(int(row[0]))
    
    c.card_ids = collection_cards

    return c


#returns ALL the collections of cards from the exported databases
def getAllCollections():
    if not __EXPORTS:
        raise ValueError("No exported databases found.")

    collections = []

    for db in __EXPORTS:
        conn = sqlite3.connect(db)
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT lists._id, lists.name, lists.creation, lists._id FROM lists")
            rows = cursor.fetchall()
        finally:
            conn.close()
        
        for row in rows:
            collections.append(Collection(name=row[1], id=row[3], created_at=None))
    
    return collections

#----------------------------------------------------------
# Test the dbutils.py
#----------------------------------------------------------
if __name__ == '__main__':
    print("Master DB: %s" % findMasterDB())
    setMasterDB(None)

    __EXPORTS = findExportedDBs()
    print("exported DBs: %s" % __EXPORTS)

    getAllCards()
    print("All cards: %d" % len(getAllCards()))
    print("First 10 cards:")
    for i, card in enumerate(getAllCards().values()):
        if i >= 10:
            break
        print(card)

    all_collections = getAllCollections()
    print("All collections: %d" % len(all_collections))
    for i in range(10):
        if i >= len(all_collections):
            break
        print(all_collections[i])

    if len(all_collections) > 0:
        collection = getCollectionCards(all_collections[0])
        print("Collection: %s" % collection)
        for i in range(10):
            if i >= len(collection.card_ids):
                break
            print(f"{collection.card_ids[i]} => { getAllCards()[collection.card_ids[i]] } { getAllCards()[collection.card_ids[i]].scryfall_id } ")