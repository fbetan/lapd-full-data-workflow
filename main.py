import pandas as pd
import numpy as np


def main():
    file_path = "/Users/franciscobetancourt/Downloads/Crime_Data_from_2020_to_Present.csv"
    df = pd.read_csv(file_path)

    columns_to_drop = [
        'DR_NO', 'Crm Cd Desc', 'Weapon Desc',
        'Premis Desc', 'Status Desc', 'Crm Cd 1'
    ]

    cleaner_df = df.drop(columns_to_drop, axis=1)

    new_dates = [date[:10] for date in cleaner_df['DATE OCC'].values]

    cleaner_df['date_occurred'] = new_dates

    columns_to_drop = [
        'DATE OCC', 'AREA', 'AREA NAME',
        'LOCATION', 'Cross Street'
    ]

    more_cleaner_df = cleaner_df.drop(columns_to_drop, axis=1)

    # Taking care of all the remaining null values

    # Vict Sex/Descent have the same number of null values, suggests these are crimes against property/things
    more_cleaner_df['Vict Sex'] = more_cleaner_df['Vict Sex'].str.replace('H', 'X')
    more_cleaner_df['Vict Sex'] = more_cleaner_df['Vict Sex'].fillna('N')
    more_cleaner_df['Vict Descent'] = more_cleaner_df['Vict Descent'].fillna('N')
    more_cleaner_df['Mocodes'] = more_cleaner_df['Mocodes'].fillna(0)
    more_cleaner_df['Weapon Used Cd'] = more_cleaner_df['Weapon Used Cd'].fillna(0)
    more_cleaner_df['Crm Cd 2'] = more_cleaner_df['Crm Cd 2'].fillna(0)
    more_cleaner_df['Crm Cd 3'] = more_cleaner_df['Crm Cd 3'].fillna(0)
    more_cleaner_df['Crm Cd 4'] = more_cleaner_df['Crm Cd 4'].fillna(0)

    # Convert the floats to ints

    def convert_and_fill_nulls(series):
        series = series.convert_dtypes()
        series = series.fillna(0)
        return series

    more_cleaner_df['Premis Cd'] = convert_and_fill_nulls(more_cleaner_df['Premis Cd'])
    more_cleaner_df['Weapon Used Cd'] = convert_and_fill_nulls(more_cleaner_df['Weapon Used Cd'])
    more_cleaner_df['Crm Cd 2'] = convert_and_fill_nulls(more_cleaner_df['Crm Cd 2'])
    more_cleaner_df['Crm Cd 3'] = convert_and_fill_nulls(more_cleaner_df['Crm Cd 3'])
    more_cleaner_df['Crm Cd 4'] = convert_and_fill_nulls(more_cleaner_df['Crm Cd 4'])

    date_occurred = [pd.to_datetime(x).strftime("%m-%Y") for x in more_cleaner_df['date_occurred']]
    date_reported = [pd.to_datetime(x).strftime('%m-%Y') for x in more_cleaner_df['Date Rptd']]

    more_cleaner_df['date_occurred'] = date_occurred
    more_cleaner_df['date_reported'] = date_reported

    rename_dictionary = {
        'TIME OCC': 'time_occurred',
        'Part 1-2': 'part_offense',
        'Rpt Dist No': 'reporting_district',
        'Crm Cd': 'crime_code',
        'Mocodes': 'mo_codes',
        'Vict Age': 'victim_age',
        'Vict Sex': 'victim_sex',
        'Vict Descent': 'victim_descent',
        'Premis Cd': 'premises_code',
        'Weapon Used Cd': 'weapon_used_code',
        'Status': 'status_code',
        'Crm Cd 2': 'crime_code_2',
        'Crm Cd 3': 'crime_code_3',
        'Crm Cd 4': 'crime_code_4',
        'LAT': 'latitude',
        'LON': 'longitude'
    }

    more_cleaner_df = more_cleaner_df.rename(columns=rename_dictionary)
    more_cleaner_df = more_cleaner_df.drop('Date Rptd', axis=1)

    clean_df = more_cleaner_df[['date_occurred', 'time_occurred', 'part_offense', 'crime_code', 'crime_code_2',
                                'crime_code_3', 'crime_code_4', 'victim_age', 'victim_sex', 'victim_descent',
                                'weapon_used_code', 'premises_code', 'status_code', 'reporting_district',
                                'date_reported',
                                'mo_codes', 'latitude', 'longitude']]

    clean_df.to_csv('/Users/franciscobetancourt/Documents/lapd_clean_data.csv')


if __name__ == '__main__':
    main()
