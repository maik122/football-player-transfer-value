from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, csv

csvFilePath = "/Users/batman/Desktop/YEAR 2/software group project/Players_file.csv"
app = Flask(__name__)
app.secret_key = 'skkankcl'

@app.route('/')
@app.route('/home')
def home():
    db__init__()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()   
    
    #Selects data for the main table
    c.execute('''SELECT PLAYER_NAME, CURRENT_TEAM, WEEKLY_SALARY, CONTRACT_DURATION, GAMES_PLAYED_THIS_YEAR, GAMES_WON,
                ROUND(WEEKLY_SALARY * CONTRACT_DURATION * CAST(GAMES_WON AS FLOAT) / GAMES_PLAYED_THIS_YEAR, 2) AS TRANSFER_VALUE,
                FG1, FG2, FG3, FG4, FG5 FROM transfer_info''')
            #above is a sql query that collects all necessary data from the database, also creates some new data based on the database values
            #for the transfer value, it takes the salary*contract*winrate
            #CAST() is needed to convert games won into a float, as if it is left as an integer the transfer value just becomes 0 for some reason
    
    players = c.fetchall()   
    
    conn.commit()
    conn.close()
    #this returns the Webpage template and passes the information from the database to the page
    return render_template('index.html', players=players)
    
    
@app.route('/graphs')
def graphs():
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    c.execute('''
            UPDATE transfer_info
            SET 
            FG1 = CASE FG1 WHEN 'W' THEN 1 ELSE 0 END,
            FG2 = CASE FG2 WHEN 'W' THEN 1 ELSE 0 END,
            FG3 = CASE FG3 WHEN 'W' THEN 1 ELSE 0 END,
            FG4 = CASE FG4 WHEN 'W' THEN 1 ELSE 0 END,
            FG5 = CASE FG5 WHEN 'W' THEN 1 ELSE 0 END;
          ''')
    
    c.execute('''
        SELECT PLAYER_NAME, 
        ROUND(WEEKLY_SALARY * CONTRACT_DURATION * CAST(GAMES_WON AS FLOAT) / GAMES_PLAYED_THIS_YEAR, 2) AS W0_VALUE,
        ROUND(WEEKLY_SALARY * (CONTRACT_DURATION) * CAST(GAMES_WON + FG1 AS FLOAT) / (GAMES_PLAYED_THIS_YEAR + 1), 2) AS W1_VALUE,
        ROUND(WEEKLY_SALARY * (CONTRACT_DURATION) * CAST(GAMES_WON + FG1 + FG2 AS FLOAT) / (GAMES_PLAYED_THIS_YEAR + 2), 2) AS W2_VALUE,
        ROUND(WEEKLY_SALARY * (CONTRACT_DURATION) * CAST(GAMES_WON + FG1 + FG2 + FG3 AS FLOAT) / (GAMES_PLAYED_THIS_YEAR + 3), 2) AS W3_VALUE,
        ROUND(WEEKLY_SALARY * (CONTRACT_DURATION) * CAST(GAMES_WON + FG1 + FG2 + FG3 + FG4 AS FLOAT) / (GAMES_PLAYED_THIS_YEAR + 4), 2) AS W4_VALUE,
        ROUND(WEEKLY_SALARY * (CONTRACT_DURATION) * CAST(GAMES_WON + FG1 + FG2 + FG3 + FG4 + FG5 AS FLOAT) / (GAMES_PLAYED_THIS_YEAR + 5), 2) AS W5_VALUE
        FROM transfer_info
        ''')
    transferValues = c.fetchall()
    print(transferValues)
    
    c.execute('''SELECT PLAYER_NAME FROM transfer_info''')
    names=c.fetchall()
    
    conn.close()
    print(transferValues)

    return render_template('compare.html', names=names, transferValues=transferValues)
    
    
@app.route('/submit_report', methods=['POST'])
def submit_report():
    player_name = request.form['player_name']
    report = request.form['report']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_reports (player_name TEXT, report TEXT)')
    
    c.execute('INSERT INTO user_reports (player_name, report) VALUES (?, ?)', (player_name, report))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/admin_view')
def admin():
    return render_template('admin_view.html')

@app.route('/admin_login', methods=['GET','POST'],endpoint='admin_login')
def login():
    if request.method == 'GET':
       return render_template('admin_login.html')
   
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    
    if user == 'admin'and pwd == "pass":
        session['xxx'] = 'admin'
        return redirect('/admin_view')
    
    error = 'user name or password is incorrect '
    return render_template('admin_login.html',error=error)

def db__init__():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()   
    
    c_table = '''CREATE TABLE IF NOT EXISTS transfer_info (
        PLAYER_NAME TEXT, DATE_OF_BIRTH TEXT, GENDER TEXT,
        DATE_SIGNED_UP TEXT, CURRENT_TEAM TEXT, TEAM_LOCATION TEXT,
        TEAM_MANAGER TEXT, WEEKLY_SALARY INT, START_OF_CONTRACT TEXT,
        CONTRACT_DURATION INT, GAMES_PLAYED_THIS_YEAR INT, GAMES_WON INT,
        FG1 INT, FG2 INT, FG3 INT, FG4 INT, FG5 INT)'''   
         
    c.execute(c_table)
    
    dataQuery = c.execute('''SELECT PLAYER_NAME FROM transfer_info''')
    checkIfData = dataQuery.fetchall()

    if len(checkIfData) == 0:
        with open(csvFilePath, 'r') as f:
            reader = csv.reader(f)
            columns = next(reader)  #this skips the first row from the csv file as it is the column name row
            c.executemany('INSERT INTO transfer_info VALUES ({})'.format(', '.join(['?']*len(columns))), reader)    

    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
    