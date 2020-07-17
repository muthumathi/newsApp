import json

from flask import Flask, Response, request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = 'Muthu@123'
app.config['MYSQL_DB'] = 'news_db'

mysql = MySQL(app)


def success_response(message):
    data = {"message": message, "status": "SUCCESS"}
    result = Response(json.dumps(data), status=200, mimetype="application/json")
    return result


def failure_response(exception=None):
    if not exception:
        exception = "Server Error"
    data = {"message": exception, "status": "FAILURE"}
    result = Response(json.dumps(data), status=400, mimetype="application/json")
    return result


@app.route('/', methods=['GET'])
def home():
    cursor = mysql.connection.cursor()
    return 'Welcome to News app'


@app.route('/add-category/', methods=['POST'])
def add_category():
    try:
        category_name = request.json.get('name', None)
        if category_name is None:
            return failure_response("Category name is Missing")
        cursor = mysql.connection.cursor()
        query = "INSERT INTO category (category_name) VALUES ('{}')".format(category_name)
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return success_response("Category added Successfully")
    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/get-category/', methods=['GET'])
def get_category():
    try:
        id = request.args.get('id', None)
        if id:
            query = "SELECT * FROM category WHERE id={}".format(id)
        else:
            query = "SELECT * FROM category"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        query_data = cursor.fetchall()
        result = {"data": []}
        for iter in query_data:
            result['data'].append({"id": iter[0], "category_name": iter[1]})
        mysql.connection.commit()
        cursor.close()
        return success_response(result)
    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/add-news/', methods=['POST'])
def add_news():
    try:
        category = request.json.get('category', None)
        headline = request.json.get('headline', None)
        detail_news = request.json.get('detail_news', None)
        if not category:
            return failure_response("Category Missing")
        cursor = mysql.connection.cursor()
        query = "INSERT INTO news (category, headline, detail_news) VALUES ('{}', '{}', '{}')".format(category,
                                                                                                      headline,
                                                                                                      detail_news)
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return success_response("News Added Successfully")
    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/list-news/', methods=['GET'])
def list_news():
    try:
        category = request.args.get('category', None)

        if category:
            query = "SELECT * FROM news WHERE category='{}'".format(category)
        else:
            query = "SELECT * FROM news"

        cursor = mysql.connection.cursor()
        cursor.execute(query)
        query_data = cursor.fetchall()
        result = {"data": []}
        for iter in query_data:
            result['data'].append({"id": iter[0], "category": iter[1], "headline": iter[2], "detail_news": iter[3]})
        mysql.connection.commit()
        cursor.close()
        return success_response(result)

    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/detail-news/', methods=['GET'])
def detail_news():
    try:
        id = request.args.get('id', None)
        if not id:
            return failure_response("Missing Parameter Id")
        query = "SELECT * FROM news WHERE id={}".format(id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        query_data = cursor.fetchall()
        result = {"data": []}
        for iter in query_data:
            result['data'].append({"id": iter[0], "category": iter[1], "headline": iter[2], "detail_news": iter[3]})
        mysql.connection.commit()
        cursor.close()
        return success_response(result)
    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/update-news/', methods=['PUT'])
def update_news():
    try:
        id = request.args.get('id', None)
        headline = request.json.get('headline', None)
        detail_news = request.json.get('detail_news', None)
        query = ''
        if headline and detail_news:
            query = "UPDATE news SET headline='{}', detail_news='{}' WHERE id={}".format(headline, detail_news, id)
        if headline is None and detail_news:
            query = "UPDATE news SET detail_news='{}' WHERE id={}".format(detail_news, id)
        if headline and detail_news is None:
            query = "UPDATE news SET headline='{}' WHERE id={}".format(headline, id)


        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return success_response("News updated Successfully")

    except Exception as e:
        print(e)
        return failure_response(e)


@app.route('/delete-news/', methods=['DELETE'])
def delete_news():
    try:
        id = request.args.get('id', None)
        query = "DELETE FROM news WHERE id={}".format(id)

        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return success_response("News deleted Successfully")

    except Exception as e:
        print(e)
        return failure_response(e)


if __name__ == '__main__':
    app.run(debug=True)
