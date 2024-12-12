import unittest

import scryfall
from delverObjects import Card

class TestScryfall(unittest.TestCase):
    def test_getImageURLFromScryfallID(self):
        card = Card("1", "b4be6f22-e9e8-462a-956b-e1c78bbadacc", "Test Card", "This is a test card", "Red", "Common", "This is a ruling", "http://test.com", "1R", "Creature")
        self.assertEqual(scryfall.getImageURLFromScryfallID(card.scryfall_id, "normal").split("?")[0], "https://cards.scryfall.io/normal/front/b/4/b4be6f22-e9e8-462a-956b-e1c78bbadacc.jpg".split("?")[0])

    def test_getImageURLFromScryfallID_cache(self):
        card = Card("1", "2dea2466-5c7f-40ce-b749-100ae89d2c90", "Test Card", "This is a test card", "Red", "Common", "This is a ruling", "http://test.com", "1R", "Creature")
        self.assertEqual(scryfall.getImageURLFromScryfallID(card.scryfall_id, "normal").split("?")[0], "https://cards.scryfall.io/normal/front/2/d/2dea2466-5c7f-40ce-b749-100ae89d2c90.jpg?1557576604".split("?")[0])
        self.assertEqual(scryfall.getImageURLFromScryfallID(card.scryfall_id, "normal").split("?")[0], "https://cards.scryfall.io/normal/front/2/d/2dea2466-5c7f-40ce-b749-100ae89d2c90.jpg?1557576604".split("?")[0])


if __name__ == '__main__':
    unittest.main()