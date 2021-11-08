import unittest
from statistics import Statistics
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatistics(unittest.TestCase):
    def setUp(self):
        # annetaan Statistics-luokan oliolle "stub"-luokan olio
        self.statistics = Statistics(
            PlayerReaderStub()
        )

    def test_sort_by_points(self):
        player = self.statistics.get_players()[0]

        self.assertEqual(self.statistics.sort_by_points(player), (16))

    def test_get_players(self):
        self.assertEqual(self.statistics.get_players(), [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ])

    def test_search(self):
        player = self.statistics.search("Semenko")
        notfound = self.statistics.searc("something")

        self.assertEqual(player, Player("Semenko", "EDM", 4, 12))
        self.assertEqual(notfound, None)

    def test_team(self):
        self.assertEqual(self.statistics.team("EDM"), [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ])

    def test_top_scorers(self):
        self.assertEqual(self.statistics.top_scorers(4), [
            Player("Gretzky", "EDM", 35, 89),
            Player("Lemieux", "PIT", 45, 54),
            Player("Yzerman", "DET", 42, 56),
            Player("Kurri",   "EDM", 37, 53),
            Player("Semenko", "EDM", 4, 12)
        ])


