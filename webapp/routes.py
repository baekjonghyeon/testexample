from flask import render_template, request
import json 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
import datetime
from webapp import app

"""
Author 김윤철
Date 2020.07.21
"""

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raspberry' #mysql passsword
app.config['MYSQL_DB'] = 'schoolfood' #mysql db [show databases;]
app.config['MYSQL_PORT'] = 33906
mysql = MySQL(app)

key = "05ae7633052e44ca8329ece2812f358a" #발급받은 키
# json 파싱
def json_parse(response):
    meal_date = []
    meal_type = []
    meal = []
    json_respone = json.loads(response.text)
    json_mealServiceDietInfo = json_respone.get("mealServiceDietInfo")
    json_rows = json_mealServiceDietInfo[1]
    rows = json_rows['row']
    for row in rows:
        meal_date.append(row.get("MLSV_YMD"))
        meal_type.append(row.get("MMEAL_SC_NM"))
        meals = row.get("DDISH_NM")
        meal.append(meals.replace("<br/>", ""))
    return meal_date, meal_type, meal
    
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    quary_return = cur.execute('SELECT * FROM schooldata') #쿼리문 [schooldata를 table명으로 변경]
    rows = cur.fetchall()
    return render_template("index.html", rows=rows)

@app.route('/food', methods=['GET'])
def foor():
    now = datetime.datetime.today()
    endDates = now + datetime.timedelta(days=4)
    startDate = now.strftime('%Y%m%d')
    endDate = endDates.strftime('%Y%m%d')
    print('ip:'+str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)),str(startDate)+'-'+str(endDate))
    meal_date = []
    meal_type = []
    meal = []
    ATPT_OFCDC_SC_CODE = request.values.get("ATPT_OFCDC_SC_CODE","error")
    SD_SCHUL_CODE = request.values.get("SD_SCHUL_CODE","error")
    SCHUL_NM = request.values.get("SCHUL_NM","error")
    if ATPT_OFCDC_SC_CODE == "error" or SD_SCHUL_CODE == "error" or SCHUL_NM == "error":
        return "Parameter 1개가 누락 되었습니다" 
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY="+key+"&Type=json&pSize=50&ATPT_OFCDC_SC_CODE="+ATPT_OFCDC_SC_CODE+"&SD_SCHUL_CODE="+SD_SCHUL_CODE+"&MLSV_FROM_YMD="+startDate+"&MLSV_TO_YMD="+endDate
    response = requests.get(url)
    meal_date, meal_type, meal = json_parse(response) 
    i = len(meal)
    return render_template("meal.html", meal_date=meal_date, meal_type=meal_type, meal=meal, schoolname=SCHUL_NM, i=i)

