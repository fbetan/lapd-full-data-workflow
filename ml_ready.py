
def make_ml_ready():
    import pandas as pd
    import numpy as np

    file_path = '/Users/franciscobetancourt/Documents/lapd_clean_data.csv'

    clean_df = pd.read_csv(file_path)

    machine_ready = clean_df.drop(['crime_code_2', 'crime_code_3', 'crime_code_4', 'date_reported',
                                   'reporting_district', 'mo_codes', 'date_occurred', 'status_code'], axis=1)

    machine_ready['crime_code'] = [x // 100 for x in machine_ready['crime_code']]
    machine_ready['weapon_used_code'] = [x // 100 for x in machine_ready['weapon_used_code']]
    machine_ready['premises_code'] = [x // 100 for x in machine_ready['premises_code']]

    # Simplify victim descent into 0, 1, 2 for null, majority (white), and minority
    simple_descent = []
    for _ in machine_ready['victim_descent']:
        if _ == 'N':
            simple_descent.append(0)
        elif _ == 'W':
            simple_descent.append(1)
        else:
            simple_descent.append(2)

    machine_ready['victim_descent'] = simple_descent

    # Convert victim sex to numerical values

    from sklearn.preprocessing import LabelEncoder

    label_encoder = LabelEncoder()

    labels = ['N', 'F', 'M', 'X']
    label_encoder.fit(labels)

    machine_ready['victim_sex'] = label_encoder.transform(machine_ready['victim_sex'])

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()

    numpy_array = np.array(machine_ready['time_occurred'])
    numpy_array = numpy_array.reshape(-1, 1)

    machine_ready['time_occurred'] = scaler.fit_transform(numpy_array)

    age_scaler = MinMaxScaler()

    array = np.array(clean_df['victim_age'])
    array = array.reshape(-1, 1)

    machine_ready['victim_age'] = age_scaler.fit_transform(array)

    long_scaler = MinMaxScaler()
    lat_scaler = MinMaxScaler()

    long_array = np.array(machine_ready['longitude'])
    lat_array = np.array(machine_ready['latitude'])

    long_array = long_array.reshape(-1, 1)
    lat_array = lat_array.reshape(-1, 1)

    machine_ready['longitude'] = long_scaler.fit_transform(long_array)
    machine_ready['latitude'] = lat_scaler.fit_transform(lat_array)

    return machine_ready