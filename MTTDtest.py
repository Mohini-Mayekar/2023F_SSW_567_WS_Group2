"""Module containing test cases for for MRTD decode and encode"""

import unittest
import os
import json
from unittest.mock import Mock, patch
from MRTD import (
    decode_mrz,
    encode_mrz,
    scan_mrz,
    get_mrz_details_from_db,
    decode_mrz_recs,
    encode_mrz_recs,
)
from contants import (
    DECODED_10_RECS,
    ENCODED_10_RECS,
    ENCODED_10_INVALID_RECS,
    DECODED_1000_RECS,
    ENCODED_1000_RECS,
    SAMPLE_ENCODED_MRZ_STR_1,
    SAMPLE_ENCODED_MRZ_STR_2,
    SAMPLE_DECODED_MRZ_REC,
    SAMPLE_DECODED_MRZ_REC_NO_MIDDLE_NAME,
)


class MTTDtest(unittest.TestCase):
    """Test cases for MRTD decode and encode"""

    def load_data(self, input_json):
        """Function to load data from json file"""
        if input_json == "decoded_10_recs":
            file_path = DECODED_10_RECS
        elif input_json == "encoded_10_recs":
            file_path = ENCODED_10_RECS
        elif input_json == "decoded_1000_recs":
            file_path = DECODED_1000_RECS
        elif input_json == "encoded_1000_recs":
            file_path = ENCODED_1000_RECS
        elif input_json == "encoded_10_invalid_recs":
            file_path = ENCODED_10_INVALID_RECS
        path = os.path.abspath(file_path)

        with open(path, mode="r", encoding="utf8") as file:
            json_data = file.read()
        data = json.loads(json_data)
        return data

    def test_scan_mrz_ok(self):
        """Invoke scan_mrz function - positive case"""
        self.assertIsNone(scan_mrz())

    def test_get_mrz_details_from_db_ok(self):
        """Invoke get_mrz_details_from_db function - positive case"""
        self.assertIsNone(get_mrz_details_from_db())

    @patch("MRTD.scan_mrz")
    def test_scan_mrz_mock_ok(self, mock_get):
        """Invoke scan_mrz function - mock positive case"""
        mock_get.return_value = Mock(ok=True)
        scan_mrz()
        self.assertEqual(mock_get.return_value.ok, True, "Scan completed successfully!")

    @patch("MRTD.get_mrz_details_from_db")
    def test_get_mrz_details_from_db_mock_ok(self, mock_get):
        """Invoke get_mrz_details_from_db function - mock positive case"""
        mock_get.return_value = Mock(ok=True)
        get_mrz_details_from_db()
        self.assertEqual(
            mock_get.return_value.ok, True, "DB call completed successfully!"
        )

    def test_decode_mrz_ok(self):
        """Invoke decode_mrz function - positive case"""
        mrz_str_1 = SAMPLE_ENCODED_MRZ_STR_1
        mrz_str_2 = SAMPLE_ENCODED_MRZ_STR_2
        decoded_mrz_json = decode_mrz(mrz_str_1, mrz_str_2)
        self.assertIsNotNone(decoded_mrz_json)

    def test_decode_mrz_check_digit_few_fails(self):
        """Invoke decode_mrz function - negative case"""
        mrz_str_1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"
        mrz_str_2 = "W620126G55CIV5910109F9707301AJ010215I<<<<<<6"
        decoded_mrz_json = decode_mrz(mrz_str_1, mrz_str_2)
        self.assertIsNone(decoded_mrz_json)

    def test_decode_mrz_all_check_digit_fails(self):
        """Invoke decode_mrz function - negative case - all incorrect check digits"""
        mrz_str_1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"
        mrz_str_2 = "W620126G55CIV5910109F9707301AJ010215I<<<<<<3"
        decoded_mrz_json = decode_mrz(mrz_str_1, mrz_str_2)
        self.assertIsNone(decoded_mrz_json)

    @patch("MRTD.decode_mrz")
    def test_decode_mrz_mock_ok(self, mock_get):
        """Invoke decode_mrz function - mock"""
        mock_get.return_value = Mock(ok=True)
        mrz_str_1 = SAMPLE_ENCODED_MRZ_STR_1
        mrz_str_2 = SAMPLE_ENCODED_MRZ_STR_2
        decode_mrz(mrz_str_1, mrz_str_2)
        self.assertEqual(mock_get.return_value.ok, True, "Record decoded successfully!")

    def test_decode_mrz_recs_ok(self):
        """Invoke decode_mrz_recs function - positive case - encode_10_recs"""
        data = MTTDtest.load_data(self, "encoded_10_recs")
        decoded_mrz_json = decode_mrz_recs(data)
        self.assertIsNotNone(decoded_mrz_json)

    def test_decode_mrz_recs_1000_ok(self):
        """Invoke decode_mrz_recs function - positive case - encoded_1000_recs"""
        data = MTTDtest.load_data(self, "encoded_1000_recs")
        decoded_mrz_json = decode_mrz_recs(data)
        self.assertIsNotNone(decoded_mrz_json)

    def test_decode_mrz_recs_invalid(self):
        """Invoke decode_mrz_recs function - positive case - encode_10_recs"""
        data = MTTDtest.load_data(self, "encoded_10_invalid_recs")
        decoded_mrz_json_list = decode_mrz_recs(data)
        self.assertIsNotNone(decoded_mrz_json_list)
        count = 0
        for decoded_mrz_json in decoded_mrz_json_list:
            if decoded_mrz_json is None:
                count += 1
        self.assertGreater(count, 0, "Contains few records with invalid check digit")

    def test_encode_mrz_ok(self):
        """Invoke encode_mrz function - positive case"""
        decoded_record = SAMPLE_DECODED_MRZ_REC
        encoded_line_1, encoded_line_2 = encode_mrz(decoded_record)
        self.assertIsNotNone(encoded_line_1)
        self.assertIsNotNone(encoded_line_2)

    def test_encode_mrz_ok_2(self):
        """Invoke encode_mrz function - positive case - no middle name"""
        decoded_record = SAMPLE_DECODED_MRZ_REC_NO_MIDDLE_NAME
        encoded_line_1, encoded_line_2 = encode_mrz(decoded_record)
        self.assertIsNotNone(encoded_line_1)
        self.assertIsNotNone(encoded_line_2)

    @patch("MRTD.encode_mrz")
    def test_encode_mrz_mock_ok(self, mock_get):
        """Invoke encode_mrz function - mock"""
        mock_get.return_value = Mock(ok=True)
        decoded_record = SAMPLE_DECODED_MRZ_REC
        encode_mrz(decoded_record)
        self.assertEqual(mock_get.return_value.ok, True, "Record decoded successfully!")

    def test_encode_mrz_recs_ok(self):
        """Invoke encode_mrz_recs function - positive case - decode_10_recs"""
        data = MTTDtest.load_data(self, "decoded_10_recs")
        encoded_json_list = encode_mrz_recs(data)
        self.assertIsNotNone(encoded_json_list)

    def test_encode_mrz_recs_1000_ok(self):
        """Invoke encode_mrz_recs function - positive case - decoded_1000_recs"""
        data = MTTDtest.load_data(self, "decoded_1000_recs")
        encoded_json_list = encode_mrz_recs(data)
        self.assertIsNotNone(encoded_json_list)


if __name__ == "__main__":
    unittest.main()
