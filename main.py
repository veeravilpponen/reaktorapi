from flask import Flask
import csv

selected_country = input("Give a country: ")
selected_year = input("Give a year (1960-2018): ")
file_type = input("Select file type (co2/population): ")

co2 = '../excelit/paastot/paasto_tiedosto.csv'
population = '../excelit/vakiluvut/vakiluku_tiedosto.csv'

if file_type == 'co2':
    file_to_open = co2
elif file_type == 'population':
    file_to_open = population

with open(file_to_open, 'r') as csvfile:
    file = csv.reader(csvfile, delimiter=',')

    # loop through the rows
    for row in file:
        # fifth line is a header line
        if file.line_num is 5:
            for x in row:
                # getting index of the selected_year
                if x == selected_year:
                    year_index = row.index(x)
        # countries start after fifth line
        elif file.line_num > 5:
            country = row[0]
            if country == selected_country:
                # co2 / population of selected_country and selected_year
                print(row[year_index])


#app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return "Hello World!"
#
# if __name__ == '__main__':
#     app.run()
