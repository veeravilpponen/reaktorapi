from flask import Flask
import csv

selected_country = input("Give a country: ")

with open('../excelit/vakiluvut/vakiluku_tiedosto.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        if lines.line_num > 4:
            country = row[0]
            if country == selected_country:
                print(row)

#app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return "Hello World!"
#
# if __name__ == '__main__':
#     app.run()
