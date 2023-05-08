from fileinput import filename
from flask import Flask,render_template,redirect,request,flash,url_for,send_file,send_from_directory
#for file uploading..
import urllib.request
import os
from werkzeug.utils import secure_filename

import mysql.connector as mysql
#obj..
app=Flask(__name__)
mydb=mysql.connect(
    host='localhost',
    user='root',
    password='Ksb6419*',
    database='showri'
)
cursor=mydb.cursor()

UPLOAD_FOLDER='static'
app.secret_key='1111'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#filename=''
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#handlers...


@app.route('/')
def start():
    return render_template('home.html')

#guest....
@app.route('/guest')
def home():
    return render_template('guest.html')

@app.route('/greg')
def greg():
    return render_template('guest-reg.html')

@app.route('/glogin')
def glogin():
    return render_template('guest-sign.html')


#user...
@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/ureg')
def ureg():
    return render_template('user-reg.html')

@app.route('/ulogin')
def ulogin():
    return render_template('user-sign.html')




#form data..

#user reg
@app.route('/urdata',methods=['post'])
def urdata():
    name=request.form['name'].strip()
    password=request.form['pass'].strip()
    branch=request.form['branch'].strip()
    phno=request.form['phone'].strip()
    sql='select * from user'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if (i[1]==password and (i[0]==name.upper() or i[0]==name.lower())):
            return render_template('user-reg.html',e='user already registred')

    s='insert into user(name,password,branch,phno)values(%s,%s,%s,%s)'
    v=(name,password,branch,phno)
    cursor.execute(s,v)
    mydb.commit()
    return render_template('user-reg.html',s='signup successfully')

#user login..
@app.route('/usdata',methods=['post'])
def usdata():
    name=request.form['name'].strip()
    password=request.form['pass'].strip()
    phno=request.form['phno'].strip()
    sql='select * from user'
    cursor.execute(sql)
    d=cursor.fetchall()
    flag=0
    for i in d:
        if(i[3]==phno):  
            
            flag=1
            return render_template('gone.html')
            #if user login success then all feedbacks will be on the user success page..
                #return render_template('feedback.html',n=name,f=fback)
    if(flag==0):
        return render_template('user-reg.html',lf='Please signup first')



#guest one....
@app.route('/gone',methods=['post'])
def gone():
    name=request.form['name'].strip()

    #guests data..feedback
    s2='select * from feedback'
    cursor.execute(s2)
    f=cursor.fetchall()
    data=[]
    flag=0
    for j in f:
        if name==j[0]:
            flag=1
            name=j[0].strip()
            fback=j[1].strip()
            filename=j[2].strip()
            dummy=[]
            dummy.append(name)
            dummy.append(fback)
            dummy.append(filename)
            data.append(dummy)
            return render_template('gones.html',data=data)
            #print(data)
    if(flag==0):
        return render_template('gone.html',de='Not found with that Guest Name')


@app.route('/gones',methods=['post'])
def gones():
    name=request.form['name'].strip()

    #guests data..feedback
    s2='select * from feedback'
    cursor.execute(s2)
    f=cursor.fetchall()
    data=[]
    flag=0
    for j in f:
        if name==j[0]:
            flag=1
            name=j[0].strip()
            fback=j[1].strip()
            filename=j[2].strip()
            dummy=[]
            dummy.append(name)
            dummy.append(fback)
            dummy.append(filename)
            data.append(dummy)
            return render_template('gones.html',data=data)
            #print(data)
    if(flag==0):
        return render_template('gones.html',de='Guest Not Found')

    

#guest reg

@app.route('/grdata',methods=['post'])
def grdata():
    name=request.form['name'].strip()
    password=request.form['pass'].strip()
    topic=request.form['topic'].strip()
    phno=request.form['phone'].strip()
    sql='select * from guest'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if (i[1]==password and (i[0]==name.upper() or i[0]==name.lower())):
            return render_template('guest-reg.html',e='You are  already registred')

    s='insert into guest(name,password,topic,phno)values(%s,%s,%s,%s)'
    v=(name,password,topic,phno)
    cursor.execute(s,v)
    mydb.commit()
    return render_template('guest-reg.html',s='signup successfully')


@app.route('/gsdata',methods=['post'])
def gsdata():
    name=request.form['name'].strip()
    password=request.form['pass'].strip()
    sql='select * from guest'
    cursor.execute(sql)
    d=cursor.fetchall()
    for i in d:
        if(i[1]==password):
            return render_template('gfeedback.html')
    return render_template('guest-sign.html',lf='Please signup in the guest registration')


#guest feedback...handling..
@app.route('/gf',methods=['post'])
def gf():
    #global filename
    name=request.form['name'].strip()
    fback=request.form['fd'].strip()
    #file...
    if 'file' not in request.files:
        return render_template('gfeedback.html',f=" file Not Avilable")
    file = request.files['file']
    if file.filename == '':
        return render_template('gfeedback.html',f='No image selected for uploading')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #here file secure with its name...
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file_url=url_for('get_file',filename=filename)

        #print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded')
    else:
        return render_template('gfeedback.html',f="'Allowed image types are - png, jpg, jpeg, gif'")
    #file uploaded ...into static/folder name
    s='insert into feedback(name,fback,filename)values(%s,%s,%s)'
    v=(name,fback,str(filename).strip())
    cursor.execute(s,v)
    mydb.commit()
    return render_template('gfeedback.html',s='Thank you for your feedback')#,filename=filename



#guest book..
@app.route('/guestbook')
def guestbook():
    s2='select * from feedback'
    cursor.execute(s2)
    f=cursor.fetchall()
    data=[]
    for j in f:
        name=j[0].strip()
        fback=j[1].strip()
        filename=j[2].strip()
        dummy=[]
        dummy.append(name)
        dummy.append(fback)
        dummy.append(filename)
        data.append(dummy)
    return render_template('guestbook.html',data=data)

   


#server start..

if __name__=='__main__':
    app.run(debug=True)


'''@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path)'''




