from flask import Flask, jsonify
from flask_cors import CORS
import csv
from flask import request

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

co2 = '../excelit/paastot/paasto_tiedosto.csv'
po = '../excelit/vakiluvut/vakiluku_tiedosto.csv'

# REQUESTS
@app.route('/compare', methods=['POST'])
def compare():
        post_data = request.get_json()
        selected_country1 = post_data['data']['country1']
        selected_country2 = post_data['data']['country2']
        per_capita = post_data['data']['percapita']

        # initialize some variables
        results = []
        years = []
        emissions = []
        emissions2 = []
        population1 = []
        population2 = []

        # results must remain empty, if the "country" option is following, so the table remains empty
        if selected_country1 and selected_country2 != "Search / select a country":

            # opening the file
            with open(co2, 'r') as csvfile:
                cofile = csv.reader(csvfile, delimiter=',')

                # loop through the rows of the file and read years into array
                for row in cofile:
                    if cofile.line_num is 5:
                        years = row[5:-1]
                    # countries start after fifth line
                    elif cofile.line_num > 5:
                        country = row[0]
                        if country == selected_country1:
                            # co2 of selected_country1
                            emissions1 = row[5:-1]
                        elif country == selected_country2:
                            # co2 of selected_country2
                            emissions2 = row[5:-1]

                timesToLoop = len(years)

            with open(po, 'r') as csvfile2:
                pofile = csv.reader(csvfile2, delimiter=',')

                if per_capita == True:
                    for row in pofile:
                        if pofile.line_num > 5:
                            country = row[0]
                            if country == selected_country1:
                                # population of selected_country1
                                population1 = row[5:-2]
                                for x in range(len(population1)):
                                    population1[x] = float(population1[x])
                                    if emissions1[x] == "":
                                        emissions1[x] = 0
                                    emissions1[x] = float(emissions1[x])
                                emissions1 = [x/y for x,y in zip(emissions1,population1)]
                            elif country == selected_country2:
                                # population of selected_country2
                                population2 = row[5:-2]
                                print(len(population2))
                                for x in range(len(population2)):
                                    population2[x] = float(population2[x])
                                    if emissions2[x] == "":
                                        emissions2[x] = 0
                                    emissions2[x] = float(emissions2[x])
                                emissions2 = [x/y for x,y in zip(emissions2,population2)]

        results = {"years":years, "countries": [{"name": selected_country1, "data": emissions1},{"name": selected_country2, "data": emissions2}]}

        return jsonify({'results':results})


# list of countries
@app.route('/countries', methods=['GET'])
def countries():
    with open(po, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        countries = []
        countries.append({"text": "Search / select a country"})
        for row in file:
            if file.line_num > 5:
                country = {"text": row[0]}
                countries.append(country)
    return jsonify({'countries':countries})

# emissions by country and optionally per capita
@app.route('/emissions', methods=['POST'])
def byCountry():
    post_data = request.get_json()
    selected_country1 = post_data['data']['country1']
    selected_country2 = post_data['data']['country2']
    per_capita = post_data['data']['percapita']

    selected_country = ''
    if selected_country1 is None:
        selected_country = selected_country2
    else:
        selected_country = selected_country1

    # initialize some variables
    results = []
    years = []
    emissions = []
    population = []

    # results must remain empty, if the "country" option is following, so the table remains empty
    if selected_country != "Search / select a country":

        # opening the file
        with open(co2, 'r') as csvfile:
            cofile = csv.reader(csvfile, delimiter=',')

            # loop through the rows of the file and read years into array
            for row in cofile:
                if cofile.line_num is 5:
                    years = row[5:-1]
                    print(years)
                # countries start after fifth line
                elif cofile.line_num > 5:
                    country = row[0]
                    if country == selected_country:
                        # co2 of selected_country
                        emissions = row[5:-1]

            timesToLoop = len(years)

        with open(po, 'r') as csvfile2:
            pofile = csv.reader(csvfile2, delimiter=',')

            if per_capita == True:
                for row in pofile:
                    if pofile.line_num > 5:
                        country = row[0]
                        if country == selected_country:
                            # population of selected_country
                            population = row[5:-1]
                            print(len(population))
                            # change population and emission values to float
                            for x in range(len(population)):
                                population[x] = float(population[x])
                                if emissions[x] == "":
                                    emissions[x] = 0
                                emissions[x] = float(emissions[x])
                            emissions = [x/y for x,y in zip(emissions,population)]

        results = {"years":years, "countries": [{"name": selected_country, "data": emissions}]}

    return jsonify({'results':results})

if __name__ == '__main__':
    app.run()
