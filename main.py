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
    selected_country = post_data['data']['country']
    per_capita = post_data['data']['percapita']

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
                    years = row[5:]
                    years = years[::-1]
                    years = years[1:]
                # countries start after fifth line
                elif cofile.line_num > 5:
                    country = row[0]
                    if country == selected_country:
                        # co2 of selected_country
                        emissions = row[5:]
                        emissions = emissions[::-1]
                        emissions = emissions[1:]

            timesToLoop = len(years)

        with open(po, 'r') as csvfile2:
            pofile = csv.reader(csvfile2, delimiter=',')

            if per_capita == True:
                for row in pofile:
                    if pofile.line_num > 5:
                        country = row[0]
                        if country == selected_country:
                            # population of selected_country
                            population = row[5:]
                            population = population[::-1]
                            population = population[1:]

            for i in range(timesToLoop):
                year = years[i]
                emission = emissions[i]

                # if emission is empty, set - as a value, table in Vue will be clearer this way
                if emission == "":
                    emission = "-"
                # if per_capita is true divide emissions by population
                elif per_capita == True:
                    # have to change string to float, before changing numbers of decimals
                    emission = format(float(emissions[i]) / float(population[i]), ".5f")
                else:
                    # change string to float, before changing numbers of decimals
                    emission = format(float(emissions[i]), ".2f")

                result = {"year": year, "emissions": emission}
                results.append(result)

    return jsonify({'results':results})

if __name__ == '__main__':
    app.run()
