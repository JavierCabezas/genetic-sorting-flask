class Reader:

    def __init__(self, number_of_preferences :int):
        self.number_of_preferences = number_of_preferences

    def transform_column_to_preference(self, column_number: int) -> int:
        """
        Gets the column number in the file and returns the preference value associated to it
        Ex: If there are two preferences then the columns 2 and 3 are going to be the first two preferences and
            columns 4 and 5 are going to be the first de-pref and second de-pref. So:

        +---------------+------------+
        |  Column num   | Return val |
        +---------------+------------+
        |       2       |      1     |
        |       3       |      2     |
        |       4       |      -1    |
        |       5       |      -2    |
        +---------------+------------+

        :param column_number:
        :param number_of_preferences:
        :return:
        """

        is_negative_pref = column_number - 1 > self.number_of_preferences
        if is_negative_pref:
            return -1 * (column_number - 1 - self.number_of_preferences)
        else:
            return column_number - 1