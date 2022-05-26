from flask import Flask, render_template, request
from flask import redirect, url_for, abort, g
import pickle
import io
import base64

app = Flask(__name__)
#decorator
@app.route('/')
def main():
    return render_template('main.html')


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        # if the user submits the form
        try:
            insert_message(request)
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)


@app.route('/view_messages/', methods=['POST', 'GET'])
def view_messages():
    if request.method == 'GET':
        return render_template('view.html')
    else:
        try:
            out = random_messages(request.form["number"]) # a format html script in string form
            return render_template('view.html', output = out) 
        except:
            return render_template('view.html', error = True)

def get_message_db():
    # write some helpful comments here
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = """
            CREATE TABLE IF NOT EXISTS message_table(
            id INTEGER, 
            handle TEXT, 
            message TEXT
            )
            """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
    return g.message_db


def insert_message(request):
    name = request.form["name"]
    message = request.form["message"]

    #opens a connection to data base
    conn = get_message_db()
    cur = conn.cursor()


    cmd = "SELECT COUNT(*) FROM message_table"
    cur.execute(cmd)
    id = cur.fetchone()[0] + 1

    cmd2 = """
        INSERT INTO message_table
        (id, handle, message)
        VALUES
        (?, ?, ?)
        """
    data = (id, name, message)
    cur.execute(cmd2, data)

    #commits the change
    conn.commit()
    #closes the connection
    conn.close()


def random_messages(n):
    """
    randomly retrieves n messages from our data base, if not enough is stored, returns all current messages
    """
    
    #opens a connection to data base
    conn = get_message_db()
    cur = conn.cursor()

    length_cmd = "SELECT COUNT(*) FROM message_table"
    cur.execute(length_cmd)
    num_len = cur.fetchone()[0]
    
    res = ""

    if (int(n) > num_len):
        res = ("We currently do not have enough messages. We can only show you this many.")
        n = str(num_len)

    cmd = "SELECT * FROM message_table ORDER BY RANDOM() LIMIT " + n

    for row in cursor_obj.execute(cmd): 
        res += row[2] + "<br>" + "- " + row[1] + "<br><br>"
    
    #closes the connection
    conn.close() 
    return res 