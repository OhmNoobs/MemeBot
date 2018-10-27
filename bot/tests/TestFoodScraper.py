import io
import unittest

from functions import food_scraper
from tests.test import PATH_TO_RESOURCES


class TestFoodScraper(unittest.TestCase):

    def test_cached_food_pages(self):
        cached_pages_paths = PATH_TO_RESOURCES.glob('food_page_*.txt')
        cached_results_paths = PATH_TO_RESOURCES.glob('parsed_food_page_*.txt')
        actual_results = self.fetch_actual_results(cached_pages_paths)
        expected_results = self.fetch_expected_results(cached_results_paths)
        for expected_result, actual_result in zip(expected_results, actual_results):
            self.assertEqual(expected_result, actual_result)

    @staticmethod
    def fetch_actual_results(cached_pages_paths):
        actual_results = []
        for path in cached_pages_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as soup_file:
                soup = soup_file.read().replace('\r', '').replace('\n', '')
                meals = food_scraper.cook_meals(soup)
                feast = food_scraper.dish_up(meals)
                actual_results.append(feast)
        return actual_results

    @staticmethod
    def fetch_expected_results(cached_results_paths):
        expected_results = []
        for path in cached_results_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as result_file:
                expected_results.append(result_file.read())
        return expected_results
