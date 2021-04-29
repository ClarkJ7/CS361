from flask import Flask
from flask_restful import Api, Resource, abort
from bs4 import BeautifulSoup
import csv, requests


app = Flask(__name__)
api = Api(app)


def check_link(page):
    if page.status_code > 200:
        abort(404, message="Bad Link")
    else:
        print("Page loaded successfully")


class ReturnTest(Resource):

    def get(self, URL):
        link = URL
        filename = "test.csv"

        page = requests.get(link)
        check_link(page)

        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find("div", {"class": "mw-parser-output"})
        ingredients = body.find_all("ul")

        with open(filename, "w") as output:
            writer = csv.writer(output)
            for row in ingredients:
                cell = []
                text = row.get_text()
                cell.append(text)
                if cell:
                    print(text)
                    writer.writerow(cell)

        return "Table Output"


api.add_resource(ReturnTest, "/<string:URL>")


if __name__ == "__main__":
    app.run(debug=True)