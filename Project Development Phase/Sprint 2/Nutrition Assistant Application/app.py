import ibm_db
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pbx92737;PWD=SYPeoksfgWh5qLcA;","","")
print("connection succesful")

app = Flask(__name__)

@app.route('/')
@app.route('/Main')
def Main():
  return render_template('Main.html')

@app.route('/about')
def about():
  return render_template('about.html') 

@app.route('/service')
def service():
  return render_template('service.html')  

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/confirm',methods = ['POST', 'GET'])
def confirm():
  if request.method == 'POST':

    email = request.form['email']
    password = request.form['password']
    sql = "SELECT * FROM login WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('list.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO login VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, email)
      ibm_db.bind_param(prep_stmt, 2, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('list.html', msg="Student Data saved successfuly..")  


if __name__=='__main__':
    app.run(debug=True)  


