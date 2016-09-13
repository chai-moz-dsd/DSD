import logging


def validate_values(date_element_values):
    count = 0
    for value in date_element_values:
        print(value)

        if count == 10:
            break

        count += 1
