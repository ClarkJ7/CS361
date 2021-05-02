from flask import Flask
from flask_restful import Api, Resource, abort
from bs4 import BeautifulSoup
import csv, requests
import pandas
import lxml


app = Flask(__name__)
api = Api(app)


def check_link(page):
    if page.status_code > 200:
        abort(404, message="Bad Link")
    else:
        print("Page loaded successfully")


class ReturnTest(Resource):

    def get(self, search, table_num):
        # Obtain wikipedia URL and designate CSV output
        link = "https://en.wikipedia.org/wiki/" + search
        filename = search + ".csv"

        # Verify wikipedia link works, abort if not
        page = requests.get(link)
        check_link(page)

        # Obtain tables into panda dataframe
        dfs = pandas.read_html(link)

        # Write desired table into CSV
        dfs[table_num].to_csv(filename)
        test = dfs[table_num]
        test_send = test.to_dict()

        return test_send


api.add_resource(ReturnTest, "/<string:search>/<int:table_num>")


if __name__ == "__main__":
    app.run(debug=True, port=5001)