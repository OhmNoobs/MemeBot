import io
import unittest

from functions import food_scraper
from tests.test import PATH_TO_RESOURCES


class TestFoodScraper(unittest.TestCase):

    def test_cached_food_pages(self):
        cached_pages_paths = PATH_TO_RESOURCES.glob('food_page_*.txt')
        cached_results_paths = PATH_TO_RESOURCES.glob('parsed_food_page_*.txt')
        actual_results = self.generate_results(cached_pages_paths)
        expected_results = self.read_expected_results(cached_results_paths)
        for i in range(1, len(actual_results)+1):
            self.assertEqual(actual_results[i], expected_results[i])

    @staticmethod
    def generate_results(cached_pages_paths):
        actual_results = {}
        for path in cached_pages_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as soup_file:
                soup = soup_file.read().replace('\r', '').replace('\n', '')
                meals = food_scraper.cook_meals(soup)
                feast = food_scraper.dish_up(meals)
                test_number = TestFoodScraper.get_resource_number(soup_file.name)
                actual_results[test_number] = feast
        return actual_results

    @staticmethod
    def read_expected_results(cached_results_paths):
        expected_results = {}
        for path in cached_results_paths:
            with io.open(str(path), mode="r", encoding="utf-8") as result_file:
                test_number = TestFoodScraper.get_resource_number(result_file.name)
                expected_results[test_number] = result_file.read()
        return expected_results

    @staticmethod
    def get_resource_number(filename):
        return int(filename[-5:-4])
