from flask import Flask, json, jsonify
from flask.globals import request
import flask
#Import the python driver for PostgreSQL
import psycopg2
from flask_cors import CORS, cross_origin
import hashlib
import socket
from flask import *  

app = Flask(__name__)
CORS(app, supports_credentials=True)

#cors = CORS(app, resources={    r"/*":{        "origins": "*"    }})

#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

@app.route("/")
def home():
    
    return "Hello, World!"




#@app.route("/head",methods=['GET'])
def head():
    headers = flask.request.headers
    
    if (headers['Token']) == "0000":
        return str(1)
    else:
        return str(0)
    
    #print(headers['Token'])
    #return "Request headers:\n" + str(headers)





@app.route("/signup",methods=['POST'])
def signup():

    if head() == "0":
        return "Invalid Attempt!"

    data = request.get_json(force=True)
    userid = data['userid']
    pswrd = data['pswrd']

    #UserID & Password Validation to check if they were empty or not.
    if not userid:
        return "The userid is empty!"
    if not pswrd:
        return "The Password is empty!"


    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "rudder",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        #To check if user already exists or not

        # Create a cursor object
        cursor = connection.cursor()
        # A sample query of all data from the "vendors" table in the "suppliers" database
        cursor.execute("""SELECT * FROM employee""")
        records = cursor.fetchall()
        flag = 0
        for row in records:
            if row[0] == userid:
                flag = 1
                break
        if flag == 1:            
            return "User Already exists kindly try with different Userid"   

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    
   
    processjson()
    return "Sucessfully Inserted!"








@app.route("/login",methods=['POST'])
def login():


    if head() == "0":
        return "Invalid Attempt!"


    data = request.get_json(force=True)
    userid2 = data['userid']
    pswrd = hashpassword(data['pswrd'])
    print("Password is: ",data['pswrd'])    
    
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "rudder",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        # Create a cursor object
        cursor = connection.cursor()
        #cursor = connection.cursor()

        # A sample query of all data from the "vendors" table in the "suppliers" database
        #cursor.execute("""SELECT * FROM employee EXCEPT SELECT * FROM   employee WHERE  userid = 'root'""")
        cursor.execute("""SELECT * FROM employee""")
        records = cursor.fetchall()
        flag = 0
        for row in records:
            #print(row[0],"    ",row[1])
            if row[0] == userid2 and row[1] == pswrd:
                #print("Matched")
                flag = 1
                break
        if flag == 0:
            print(userid2,"    ",pswrd)
            return "Invalid UserID and/or Password. Please try again!!"
        
        else: 
            res = make_response('http://127.0.0.1:5500/listuser.html')
            res.set_cookie('username',userid2, max_age=604800, samesite='Lax', secure=None, httponly=None)
            print("username  ",request.cookies.get('username'))
            print("userid2 = ",userid2)
            #return "Succesfully logged in. Userid & Password matched!"
            #return render_template('http://127.0.0.1:5500/listuser.html')
            #return res #redirect(url_for('listuser'))
            return res

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    return "Succesfull!"


@app.route("/listuser",methods=['GET'])
def listuser():
    
    if head() == "0":
        return "Invalid Attempt!"

    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "rudder",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        # Create a cursor object
        cursor = connection.cursor()
        #cursor = connection.cursor()

        # A sample query of all data from the "vendors" table in the "suppliers" database
        tempcookie = request.cookies.get('username')
        print("Cookie: ",tempcookie)
        if tempcookie != 'root':
            cursor.execute("""SELECT userid,fname,lname FROM employee EXCEPT SELECT userid,fname,lname FROM   employee WHERE  userid = 'root'""")
        else:
            cursor.execute("""SELECT * FROM employee""")
        records = cursor.fetchall()
        #products=[['1','product 1'],['2','product 2']]
        arr=[]
        for product in records:
            vals = {}
            vals[' userid']=product[0]
            vals['fname']=product[1]
            vals['lname']=product[2]
            
            arr.append(vals)
        # Serializing json    
        #json_object = json.dumps(arr)   
        #print(json_object)
        #print((arr))
        #print(records)
        return jsonify(arr)

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    return "Succesfull!"


@app.route("/delete",methods=['POST'])
def delete():

    if head() == "0":
        return "Invalid Attempt!"

    tempcookie = request.cookies.get('username')
    print("Cookie: ",tempcookie)
    if tempcookie != 'root':
        return "Invalid attempt!"
    
    data = request.get_json(force=True)
    userid = data['userid']        

    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "rudder",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        # Create a cursor object
        cursor = connection.cursor()
        #cursor = connection.cursor()

        # A sample query of all data from the "vendors" table in the "suppliers" database
        cursor.execute("DELETE FROM employee WHERE userid = %s",(userid))
        rows_deleted = cursor.rowcount
        connection.commit()
        print("Userid: ",userid)
        if rows_deleted >= 1:
            return "Deleted Successfully!"
        else:
            return "Not Deleted!"

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    return "Not Succesfull!"

#@app.route("/processjson",methods=['POST'])
def processjson():

    data = request.get_json(force=True)
    userid = data['userid']
    pswrd = hashpassword(data['pswrd'])
    fname = data['fname']
    lname = data['lname']
 
    #Create a connection credentials to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "rudder",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )


        cursor = connection.cursor()
        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        #cursor = connection.cursor()
    
        pg_insert = """ INSERT INTO employee (userid, pswrd, fname, lname) VALUES (%s,%s,%s,%s)"""
        #inserted_values = ('2', '12345678', 'Mark', 'Zuckerberg')
        inserted_values = (userid, pswrd, fname, lname)

        cursor.execute(pg_insert, inserted_values)
        connection.commit()

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    return "Succesfully Inserted!"


def hashpassword(pswrd):
    pswrd=hashlib.md5(pswrd.encode()).hexdigest()
    pswrd=str(pswrd)
    return pswrd



if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='127.0.0.1:5500', port=8000, debug=True)
