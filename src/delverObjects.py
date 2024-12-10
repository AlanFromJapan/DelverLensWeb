import datetime

class Collection:
    def __init__(self, name, id, description=None, card_ids=None, created_at=None):
        self.name = name
        self.id = id
        self.description = description
        self.card_ids = card_ids

        #assume std unix timestamp
        if created_at is not None:
            self.created_at = datetime.datetime.fromtimestamp(created_at)
        else:
            self.created_at = created_at

    def __str__(self):
        return f"{self.name} #{ self.id } [{len(self.card_ids) if self.card_ids else 0} cards]"
    

#-------------------------------------------------------------
class Card:
    def __init__(self, id, scryfall_id=None, name=None, description=None, color=None, rarity=None, ruling=None, image=None, mana=None, type=None):
        self.id = id
        self.scryfall_id = scryfall_id
        self.name = name
        self.description = description
        self.color = color
        self.rarity = rarity
        self.ruling = ruling
        self.image = image
        self.mana = mana
        self.type = type

    def __str__(self):
        return f"{self.name} [{self.id}]"