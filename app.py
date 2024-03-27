from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Resource, Api, reqparse
from azuresqlconnector import *
import requests


app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index2():
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = """SELECT PotholeID, Latitude, Longitude FROM Potholes.PotholeLocation"""
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()
    return render_template('index.html', records = records)

@app.route('/edit.html')
def index3():
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = """SELECT PotholeID, Latitude, Longitude FROM Potholes.PotholeLocation"""
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()

    return render_template('edit.html', records = records)


@app.route('/edit.html', methods=['POST'])
def edit_entry():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'delete':
            pothole_id = request.form.get('PotholeID')
            conn = SQLConnection()
            conn = conn.getConnection()
            cursor = conn.cursor()
            delete_query = """DELETE FROM Potholes.PotholeLocation WHERE PotholeID = ?"""
            cursor.execute(delete_query, (pothole_id,))
            conn.commit()
            cursor.close()
            return "Entry deleted successfully"
        
        elif action == 'add':
            pothole_id = request.form.get('PotholeID')
            latitude = request.form.get('Latitude')
            longitude = request.form.get('Longitude')
            conn = SQLConnection()
            conn = conn.getConnection()
            cursor = conn.cursor()
            insert_query = """INSERT INTO Potholes.PotholeLocation (PotholeID, Latitude, Longitude) VALUES (?, ?, ?)"""
            cursor.execute(insert_query, (pothole_id, latitude, longitude))
            conn.commit()
            cursor.close()
            return "Entry added successfully"


if __name__ == "__main__":
    app.run(debug=True)