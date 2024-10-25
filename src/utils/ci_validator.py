
"""
 Description: CIValidator class is responsible for validating the CI number of a person in Uruguay.

 Date: 2024-10-18
 """
class CIValidator:
    """
    Description: This method is responsible for validating the CI number of a person in Uruguay.

    Parameters:
        ci_param (str): The CI number of a person in Uruguay.

    Returns:
        bool: True if the CI number is valid, False otherwise.
    """
    def is_valid(ci_param: str):
        ci = str(ci_param).replace("-", "").replace(".", "")
        ci = ci.zfill(8)
        check_digit_param = int(ci[-1])
        ci_number = ci[:-1]

        weights = [2, 9, 8, 7, 6, 3, 4]

        total = 0
        for i in range(7):
            digit = int(ci_number[i])
            weight = weights[i]
            total += digit * weight

        calculated_check_digit = (10 - (total % 10)) % 10

        return check_digit_param == calculated_check_digit