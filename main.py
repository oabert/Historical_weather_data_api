from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]


@app.route('/')
def home():
    return render_template('home.html', data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def weather(station, date):
    filepath = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'

    df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'], sep=",", engine="python", skipfooter=1)
    # df['    DATE'] = df['    DATE'].dt.date

    date_test = df['    DATE']

    # temp_data = df.loc[date_test == date]

    temp_data = df.loc[date_test == date]['   TG'].squeeze()

    temperature = temp_data / 10
    # temperature = 23
    temperature_dict = {'station': station,
                        'date': date,
                        'temperature': temperature}
    return temperature_dict


# @app.route('/api/v1/<station>')
# def stations(station):
#     filepath = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
#     df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
#     result = df.to_dict(orient='records')
#     return result


@app.route('/api/v1/yearly/<station>/<year>')
def yearly(station, year):
    filepath = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filepath, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='records')
    return result


# Dictionary part
filepath_d = 'dictionary.csv'
df = pd.read_csv(filepath_d)


@app.route('/dict')
def dictionary():
    return render_template('dictionary.html')


@app.route('/api/dict/<word>')
def dictionary_api(word):
    definition = df.loc[df['word'] == 'word']['definition'].squeeze()
    result = {'word': word, 'definition': definition}
    return result


if __name__ == '__main__':
    app.run(debug=True)
