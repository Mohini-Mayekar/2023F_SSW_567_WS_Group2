"""Constants"""

DECODED_10_RECS = "records_decoded_10.json"
ENCODED_10_RECS = "records_encoded_10.json"
ENCODED_10_INVALID_RECS = "records_encoded_10_with_invalid_entries.json"
DECODED_1000_RECS = "records_decoded_1000.json"
ENCODED_1000_RECS = "records_encoded_1000.json"

CHECK_DIGIT_VERIFICATION_FAILED = "Check digit verification failed"
CHECK_DIGIT_VERIFICATION_FAILED_DETAILS = ("Check digit verification failed for '{field}' field"
                                           " with '{value}' value in record. "
                                           "Expected: '{expected}', received: '{received}'")

SAMPLE_ENCODED_MRZ_STR_1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"
SAMPLE_ENCODED_MRZ_STR_2 = "W620126G54CIV5910106F9707302AJ010215I<<<<<<6"
SAMPLE_DECODED_MRZ_REC = (
        {
            "line1": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM",
            },
            "line2": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I",
            },
        }
    )
SAMPLE_DECODED_MRZ_REC_NO_MIDDLE_NAME = (
        {
            "line1": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH",
            },
            "line2": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I",
            },
        }
    )
