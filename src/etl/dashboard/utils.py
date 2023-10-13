from pandas import DataFrame, concat

class ColumnExpander:
    def __init__(self, unique_values: list[str], column: str) -> None:
        self.column_to_expand = column
        self.uniques = unique_values
    
    def expand(self, dataframe: DataFrame) -> DataFrame:
        values = []
        for value in dataframe[self.column_to_expand].dropna().values:
            rows = []
            for unique_value in self.uniques:
                if unique_value in value.split(','):
                    rows.append(True)
                else:
                    rows.append(False)
            values.append(rows)
        return DataFrame(values, columns=self.uniques)
    
    # def expand(self, dataframe: DataFrame) -> DataFrame:
    #     expanded_columns = self.__one_hot_encode(dataframe)
    #     dataframe = concat([dataframe, expanded_columns], axis=1)
    #     return dataframe.drop(columns=self.column_to_expand)
