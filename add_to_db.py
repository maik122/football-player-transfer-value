import csv
import sqlite3


#this is how we connect to the SQLite database
conn = sqlite3.connect('database.db')
#the cursor is just something we use to sql commands in python, it can be called anything but i usually call it c for ease
c = conn.cursor()


def db_setup():
    with open('/Users/batman/Desktop/YEAR 2/software group project/Players_file.csv', 'r') as f:
        csv_r = csv.reader(f)
        new_cols = [header.replace(' ','_') for header in csv_r.fieldnames]
        
        with open('players_updated.csv', 'w', newline='') as new_csv:
            csv_w = csv.writer(new_csv)
            csv_w.writerow(new_cols)
            
            for row in csv_r:
                csv_w.writerow(row.values())
    
    c_table = f"CREATE TABLE IF NOT EXISTS transfer_info ({','.join(new_cols)})"
    c.execute(c_table)
    
    with open('players_updated.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  #this skips the first row from the csv file as it is the column name row
        c.executemany(f"INSERT INTO transfer_info ({','.join(new_cols)}) VALUES ({','.join(['?' for _ in new_cols])})")

    #c.execute('SELECT PLAYER_NAME, CURRENT_TEAM, WEEKLY_SALARY, CONTRACT_DURATION, GAMES_PLAYED_THIS_YEAR, GAMES_WON, WEEKLY_SALARY * CONTRACT_DURATION * CAST(GAMES_WON AS FLOAT) / GAMES_PLAYED_THIS_YEAR AS TRANSFER_VALUE FROM transfer_info')
    #players = [{'player_name': row[0], 'current_club': row[1], 'weekly_salary': row[2], 'contract_duration': row[3],
    #                'games_played': row[4], 'games_won': row[5], 'transfer_value': round(row[6], 2)} for row in c.fetchall()]
   
#db_setup()
#this opens the CSV file and reads the column names as they are just the first row of the file 
#When you run this, you will need to change the path of the players_file.csv because it will be different!!!

'''
with open('C:\year 2\year 2\Systems Development\initial mockups\Players_File.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)
'''

#ALL OF THE FOLLOWING COMMANDS ARE COMMENTED OUT, UNCOMMENT THEM TO USE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#IF YOU WANT ME TO EXPLAIN ANY OF THIS TO YOU JUST ASK!!! - John ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#CREATE TABLE
#this command looks complicated but all it does is it takes the column names from the code above and creates a database with those column names
'''
create_table = 'CREATE TABLE transfer_info ({})'.format(', '.join('{} TEXT'.format(col) for col in columns))
'''
#this is how you execute the command, above you can see i define the command with a name, but we need to execute it by doing c.execute(command) c being the cursor we defined earlier
'''
c.execute(create_table)
'''


#INSERT DATA
#this command now takes the data from the csv file and inserts it into the correct columns
#again you will need to change the path of the players_file.csv for the command to work as yours will be different
'''
with open('C:\year 2\year 2\Systems Development\initial mockups\Players_File.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)  #this skips the first row from the csv file as it is the column name row
    c.executemany('INSERT INTO transfer_info VALUES ({})'.format(', '.join(['?']*len(columns))), reader)
'''



#DATA
#this just displays all information in the database - quite messy but useful just to see it
#i usually run this everytime just to make sure the database is the same as before

c.execute('''SELECT PLAYER_NAME, WEEKLY_SALARY FROM transfer_info''')
list = c.fetchall()
print(list)



#FORMATTED DATA
#this command displays all the data from the database in a more formatted way, it is also only the information we need for the main page
'''
c.execute('SELECT PLAYER_NAME, CURRENT_TEAM, WEEKLY_SALARY, CONTRACT_DURATION, GAMES_PLAYED_THIS_YEAR, GAMES_WON, WEEKLY_SALARY * CONTRACT_DURATION * CAST(GAMES_WON AS FLOAT) / GAMES_PLAYED_THIS_YEAR AS TRANSFER_VALUE FROM transfer_info')
players = [{'player_name': row[0], 'current_club': row[1], 'weekly_salary': row[2], 'contract_duration': row[3],
                'games_played': row[4], 'games_won': row[5], 'transfer_value': round(row[6], 2)} for row in c.fetchall()]
for player in players:
    print(player)    
'''


#COLUMNS
#this command looks strange but all it does is display the column names for the table as there isnt an easy way of seeing that

c.execute("PRAGMA table_info('transfer_info')")
columnsUnclean = c.fetchall()
columns = [row[1] for row in columnsUnclean]

#c.execute('SELECT PLAYER_NAME, WEEKLY_SALARY * CONTRACT_DURATION * CAST(GAMES_WON AS FLOAT) / GAMES_PLAYED_THIS_YEAR AS TRANSFER_VALUE_0 FROM transfer_info')
#transfer_values = [{'transfer_value_0': row[1]} for row in c.fetchall()]

#for value in transfer_values:
#    print(value)
'''
def calculate_transfer_value(weekly_salary, contract_duration, games_won, fg1, games_played_this_year):
    transfer_value = weekly_salary * contract_duration * (games_won + fg1) / games_played_this_year
    return transfer_value

# Retrieve the necessary data from the database
c.execute('SELECT PLAYER_NAME, WEEKLY_SALARY, CONTRACT_DURATION, GAMES_WON, FG1, GAMES_PLAYED_THIS_YEAR FROM transfer_info')
transfer_values = []
for row in c.fetchall():
    player_name = row[0]
    weekly_salary = row[1]
    contract_duration = row[2]
    games_won = row[3]
    fg1 = row[4]
    games_played_this_year = row[5]
    transfer_value = calculate_transfer_value(weekly_salary, contract_duration, games_won, fg1, games_played_this_year)
    transfer_values.append({'player_name': player_name, 'transfer_value': transfer_value})

# Print the transfer values for each player
for value in transfer_values:
    print(value)
'''
c.execute("PRAGMA table_info('transfer_info')")
columnsUnclean = c.fetchall()
columns = [row[1] for row in columnsUnclean]
print(columns)
# Commit the changes and close the database connection
conn.commit()
conn.close()
    