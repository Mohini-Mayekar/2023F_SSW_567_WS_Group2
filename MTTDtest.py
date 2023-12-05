"""Module containing test cases for for MRTD decode and encode"""

import unittest
import os
import json
from contants import DECODED_10_RECS, ENCODED_10_RECS, DECODED_1000_RECS, ENCODED_1000_RECS

class MTTDtest(unittest.TestCase):
    """Test cases for MRTD decode and encode"""

    def load_data(self, input_json):
        """Function to load data from json file"""
        if input_json == 'decoded_10_recs' :
            file_path = DECODED_10_RECS
        elif input_json == 'encoded_10_recs' :
            file_path = ENCODED_10_RECS
        elif input_json == 'decoded_1000_recs' :
            file_path = DECODED_1000_RECS
        elif input_json == 'encoded_1000_recs' :
            file_path = ENCODED_1000_RECS
        path = os.path.abspath(file_path)

        with open(path, mode="r", encoding="utf8") as file:
            json_data = file.read()
        data = json.loads(json_data)
        return data


if __name__ == "__main__":
    print("Running unit tests")
    unittest.main()
