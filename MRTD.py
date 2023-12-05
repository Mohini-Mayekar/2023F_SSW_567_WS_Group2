"""Module - encoding and decoding MRZ"""

from contants import (
    CHECK_DIGIT_VERIFICATION_FAILED,
    CHECK_DIGIT_VERIFICATION_FAILED_DETAILS
)


def scan_mrz():
    """logic to scan MRZ and return two strings - blank function"""
    #blank function
    # mrz_str_ln_1 = SAMPLE_ENCODED_MRZ_STR_1
    # mrz_str_ln_2 = SAMPLE_ENCODED_MRZ_STR_2
    # return mrz_str_ln_1, mrz_str_ln_2


def get_mrz_details_from_db():
    """logic to get MRTD information from DB - blank function"""
    # decoded_rec = SAMPLE_DECODED_MRZ_REC
    # return decoded_rec


def decode_mrz_recs(encoded_recs_json):
    """Decode multiple MRZ recs"""
    try:
        decoded_json_list = []
       # check_digit_errors = []
        encoded_recs = encoded_recs_json["records_encoded"]
        for rec in encoded_recs:
        # P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6
            mrz_str_list = rec.split(";")
            mrz_str_ln_1 = mrz_str_list[0]
            mrz_str_ln_2 = mrz_str_list[1]
            decoded_json_list.append(decode_mrz(mrz_str_ln_1, mrz_str_ln_2))

        # if check_digit_errors:
        #     raise ValueError(CHECK_DIGIT_VERIFICATION_FAILED, check_digit_errors)

        return decoded_json_list

    # except ValueError as e:
    #     #print(f"Error: {e}")
    #     if len(e.args) > 1 and isinstance(e.args[1], list):
    #         # Error contains check digit verification details
    #         check_digit_errors = e.args[1]
    #         for error in check_digit_errors:
    #             print(
    #                 CHECK_DIGIT_VERIFICATION_FAILED_DETAILS.format(
    #                     field=error[0],
    #                     value=error[1],
    #                     expected=error[2],
    #                     received=error[3],
    #                 )
    #             )
    except TimeoutError:
        print("TimeoutError - in decode_mrz_recs")


def decode_mrz(mrz_str_ln_1, mrz_str_ln_2):
    """Decode a MRZ string"""
    try:
        check_digit_errors = []

        mrz_str_ln_1_list = mrz_str_ln_1.split("<")
        # print("mrz_str_ln_1_list : ", mrz_str_ln_1_list)
        # doc_type = mrz_str_ln_1_list[0]
        issuing_country = (mrz_str_ln_1_list[1])[:3]  # first 3 char from idx 1
        last_name = (mrz_str_ln_1_list[1])[3:]  # lastname from idx 1
        first_name = mrz_str_ln_1_list[3]
        middle_name = mrz_str_ln_1_list[4]
        given_name = first_name + " " + middle_name

        # print("doc_type : ", doc_type)
        # print("issuing_country : ", issuing_country)
        # print("last_name : ", last_name)
        # print("first_name : ", first_name)
        # print("middle_name : ", middle_name)
        # print("given_name : ", given_name)

        line_1_json_str = (
            '{"issuing_country": "'
            + issuing_country
            + '", "last_name": "'
            + last_name
            + '", "given_name": "'
            + given_name
            + '"}'
        )

        # W620126G54CIV5910106F9707302AJ010215I<<<<<<6
        mrz_str_ln_2_list = mrz_str_ln_2.split("<")
        # print("mrz_str_ln_2_list : ", mrz_str_ln_2_list)
        # ['W620126G54CIV5910106F9707302AJ010215I', '','','','','','','6'] // len = 7

        # 012345678 9 10   13     19 20  21     27 28
        # W620126G5 4 CIV  591010 6  F   970730 2  AJ010215I
        mrz_str_ln_2_0 = mrz_str_ln_2_list[0]
        doc_number = mrz_str_ln_2_0[:9]  # // len = 9
        doc_check_digit = mrz_str_ln_2_0[9:10]
        calc_doc_check_digit = calculate_check_digit(doc_number)
        if doc_check_digit != calc_doc_check_digit:
            check_digit_errors.append(
                (
                    "passport number",
                    doc_number,
                    calc_doc_check_digit,
                    doc_check_digit,
                )
            )
        country_code = mrz_str_ln_2_0[10:13]
        birth_date = mrz_str_ln_2_0[13:19]  # // len = 6
        birth_date_check_digit = mrz_str_ln_2_0[19:20]
        calc_birth_date_check_digit = calculate_check_digit(birth_date)
        if birth_date_check_digit != calc_birth_date_check_digit:
            check_digit_errors.append(
                (
                    "birth date",
                    birth_date,
                    calc_birth_date_check_digit,
                    birth_date_check_digit,
                )
            )
        gender = mrz_str_ln_2_0[20:21]
        expiration_date = mrz_str_ln_2_0[21:27]  # // len = 6
        expiration_date_check_digit = mrz_str_ln_2_0[27:28]
        calc_expiration_date_check_digit = calculate_check_digit(expiration_date)
        if expiration_date_check_digit != calc_expiration_date_check_digit:
            check_digit_errors.append(
                (
                    "expiration date",
                    expiration_date,
                    calc_doc_check_digit,
                    expiration_date_check_digit,
                )
            )
        personal_number = mrz_str_ln_2_0[28:]
        personal_number_check_digit = mrz_str_ln_2_list[6]
        calc_personal_number_check_digit = calculate_check_digit(personal_number)
        if personal_number_check_digit != calc_personal_number_check_digit:
            check_digit_errors.append(
                (
                    "personal number",
                    personal_number,
                    calc_personal_number_check_digit,
                    personal_number_check_digit,
                )
            )

        # print("doc_number : ", doc_number)
        # print("doc_check_digit : ", doc_check_digit)
        # print("country_code : ", country_code)
        # print("birth_date : ", birth_date)
        # print("birth_date_check_digit : ", birth_date_check_digit)
        # print("gender : ", gender)
        # print("expiration_date : ", expiration_date)
        # print("expiration_date_check_digit : ", expiration_date_check_digit)
        # print("personal_number : ", personal_number)
        # print("personal_number_check_digit : ", personal_number_check_digit)

        line_2_json_str = (
            '{"passport_number": "'
            + doc_number
            + '", "country_code": "'
            + country_code
            + '", "birth_date": "'
            + birth_date
            + '", "sex": "'
            + gender
            + '", "expiration_date": "'
            + expiration_date
            + '", "personal_number": "'
            + personal_number
            + '"}'
        )

        json_str = '{"line1": ' + line_1_json_str + ',"line2": ' + line_2_json_str + "}"

        if check_digit_errors:
            raise ValueError(CHECK_DIGIT_VERIFICATION_FAILED, check_digit_errors)
        # print("Valid data")
        return json_str

    except ValueError as e:
        #print(f"Error: {e}")
        if len(e.args) > 1 and isinstance(e.args[1], list):
            # Error contains check digit verification details
            check_digit_errors = e.args[1]
            for error in check_digit_errors:
                print(
                    CHECK_DIGIT_VERIFICATION_FAILED_DETAILS.format(
                        field=error[0],
                        value=error[1],
                        expected=error[2],
                        received=error[3],
                    )
                )
    except TimeoutError:
        print("TimeoutError - in decode_mrz")


def encode_mrz_recs(decoded_recs_json):
    """Encode multiple MRZ recs"""
    decoded_recs = decoded_recs_json["records_decoded"]
    encoded_json_list = []
    for rec in decoded_recs:
        encoded_line_1, encoded_line_2 = encode_mrz(rec)
        encoded_json_list.append(encoded_line_1 + ";" + encoded_line_2)
    return encoded_json_list


def encode_mrz(rec):
    """Encode a MRZ string"""
    try:
        rec_line_1 = rec["line1"]
        issuing_country = rec_line_1["issuing_country"]
        last_name = rec_line_1["last_name"]
        given_name = rec_line_1["given_name"]

        if given_name.find(" ") != -1:
            name = given_name.split(" ")
            first_name = name[0]
            middle_name = name[1]
        else:
            first_name = given_name
            middle_name = ""

        # print("doc_type : ", doc_type)
        # print("issuing_country : ", issuing_country)
        # print("last_name : ", last_name)
        # print("first_name : ", first_name)
        # print("middle_name : ", middle_name)
        # print("given_name : ", given_name)

        #   P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<
        line_1 = ("P", issuing_country + last_name, first_name, middle_name)
        encoded_line_1 = (
            f"{line_1[0]}<{line_1[1]}<<{line_1[2]}<{line_1[3]}<<<<<<<<<<<<<<<<<<<<<<"
        )

        # print("encoded_line_1 : ", encoded_line_1)

        rec_line_2 = rec["line2"]
        passport_number = rec_line_2["passport_number"]
        doc_check_digit = calculate_check_digit(passport_number)
        country_code = rec_line_2["country_code"]
        birth_date = rec_line_2["birth_date"]
        birth_date_check_digit = calculate_check_digit(birth_date)
        gender = rec_line_2["sex"]
        expiration_date = rec_line_2["expiration_date"]
        expiration_date_check_digit = calculate_check_digit(expiration_date)
        personal_number = rec_line_2["personal_number"]
        personal_number_check_digit = calculate_check_digit(personal_number)

        # print("passport_number : ", passport_number)
        # print("doc_check_digit : ", doc_check_digit)
        # print("country_code : ", country_code)
        # print("birth_date : ", birth_date)
        # print("birth_date_check_digit : ", birth_date_check_digit)
        # print("gender : ", gender)
        # print("expiration_date : ", expiration_date)
        # print("expiration_date_check_digit : ", expiration_date_check_digit)
        # print("personal_number : ", personal_number)
        # print("personal_number_check_digit : ", personal_number_check_digit)

        #   W620126G54CIV5910106F9707302AJ010215I<<<<<<6
        line_2 = (
            passport_number
            + doc_check_digit
            + country_code
            + birth_date
            + birth_date_check_digit
            + gender
            + expiration_date
            + expiration_date_check_digit
            + personal_number,
            personal_number_check_digit,
        )
        encoded_line_2 = f"{line_2[0]}<<<<<<{line_2[1]}"

        # print("encoded_line_2 : ", encoded_line_2)

        return encoded_line_1, encoded_line_2

    except TimeoutError:
        print("TimeoutError - in encode_mrz")


def calculate_check_digit(data):
    """Calculate check digit for data as per the algorithm provided in the project description"""
    weighting = [7, 3, 1] * 3
    sum_of_products = 0
    for i, char in enumerate(data):
        if char.isalpha():
            numeric_val = ord(char) - ord("A") + 10
            assigned_numeric_value = numeric_val
        elif char.isnumeric():
            assigned_numeric_value = int(char)
        else:
            assigned_numeric_value = int(0)

        sum_of_products += assigned_numeric_value * weighting[i]

    # print("sum_of_products : ", sum_of_products)
    # print("check_digit : ", sum_of_products % 10)
    # check_digit
    return str(sum_of_products % 10)


# if __name__ == "__main__":
#     # Input from the scanner - mrz_str
#     MRZ_STR_1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"
#     MRZ_STR_2 = "W620126G55CIV5910106F9707302AJ010215I<<<<<<6"

#     decode_mrz(MRZ_STR_1, MRZ_STR_2)
