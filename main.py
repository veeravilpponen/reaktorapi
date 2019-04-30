from flask import Flask, jsonify
from flask_cors import CORS
import csv
from flask import request

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

# def ByCountryByYear():
#
#     selected_country = input("Give a country: ")
#     selected_year = input("Give a year (1960-2018): ")
#     file_type = input("Select file type (co2/population): ")
#
#     co2 = '../excelit/paastot/paasto_tiedosto.csv'
#     population = '../excelit/vakiluvut/vakiluku_tiedosto.csv'
#
#     # choosing between files
#     if file_type == 'co2':
#         file_to_open = co2
#     elif file_type == 'population':
#         file_to_open = population
#
#     # opening the file
#     with open(file_to_open, 'r') as csvfile:
#         file = csv.reader(csvfile, delimiter=',')
#
#         # loop through the rows of the file
#         for row in file:
#
#             # fifth line is a header line
#             if file.line_num is 5:
#                 for x in row:
#                     # getting index of the selected_year
#                     if x == selected_year:
#                         i_year = row.index(x)
#
#             # countries start after fifth line
#             elif file.line_num > 5:
#                 country = row[0]
#                 if country == selected_country:
#                     # co2 / population of selected_country and selected_year
#                     tulos = row[i_year]
#                     if tulos is "":
#                         print("No information available")
#                     elif tulos is not None:
#                         print(row[i_year])


# first request

@app.route('/countries', methods=['GET'])
def countries():
    with open('../excelit/vakiluvut/vakiluku_tiedosto.csv', 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        countries = []
        for row in file:
            if file.line_num > 5:
                countries.append(row[0])
    return jsonify({'countries':countries})

# Another request

@app.route('/country', methods=['POST'])
def ByCountry():
    post_data = request.get_json()
    selected_country  = post_data['data']['country']

    co2 = '../excelit/paastot/paasto_tiedosto.csv'
    population = '../excelit/vakiluvut/vakiluku_tiedosto.csv'

    # opening the file
    with open(co2, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=',')

        result = []
        # loop through the rows of the file
        for row in file:
            if file.line_num is 5:
                years = row[5:]
            # countries start after fifth line
            elif file.line_num > 5:
                country = row[0]
                if country == selected_country:
                    # co2 / population of selected_country
                    result = row[5:]

    return jsonify({'result':result})

if __name__ == '__main__':
    print("Server is running on localhost!")
    app.run()
