from flask import Flask
from flask_restful import Api, Resource, abort
from bs4 import BeautifulSoup
import csv, requests


app = Flask(__name__)
api = Api(app)


def abort_if_link_bad(page):
    if page.status_code > 200:
        abort(404, message="Bad Link")
    else:
        print("Page loaded successfully")


class ReturnTest(Resource):

    def get(self, search):
        link = "https://en.wikipedia.org/wiki/" + search
        #filename = search + ".csv"
        filename = "test.csv"
        print("Link is: " + link + "\n")
        #print("Filename is: " + filename + "\n")

        page = requests.get(link)
        abort_if_link_bad(page)

        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find("table", {'class': ["infobox vcard", "infobox bordered vcard"]})

        list_of_rows = []
        for row in table.find("tbody").find_all("tr"):
            list_of_cells = []
            for cell in row.find_all(["th", "td"]):
                text = cell.get_text()
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)

        with open(filename, "w") as output:
            csvwriter = csv.writer(output)
            for item in list_of_rows:
                csvwriter.writerow(item)
        return "Table Output"


api.add_resource(ReturnTest, "/<string:search>")


if __name__ == "__main__":
    app.run(debug=True)