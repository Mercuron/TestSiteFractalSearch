from flask import Flask,render_template,url_for,request,redirect,session,flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import pandas as pd
from rq import Queue
from redis import Redis
redis_conn = Redis()
queue = Queue(connection=redis_conn)
#datetime.now().strftime('%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
from sqlalchemy.sql import func
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'static/'
app.config["SECRET_KEY"]='dfhouahdf;o2ief29fj;2ijfo;ijf'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#DATABASE MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Methods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    methodname = db.Column(db.String(80), unique=True, nullable=False)
    body = db.Column(db.Text,unique=True, nullable=False)
    folder=db.Column(db.String(100),)

    def __repr__(self):
        return '<Method %r>' % self.methodname

class Method1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False )
    outputimage = db.Column(db.Text,default='pathtooutput')
    text=db.Column(db.Text,default='textfortext')
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Method %r>' % self.image
#ROUTES
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/allmethods')
def allmethods():
    return render_template('allmethods.html',methods=Methods.query.all())
@app.route('/method/<method_name>')
def method1(method_name):
    print('---METHODNAME---',method_name)
    path='/methods/'+method_name+'.html'
    method=Methods.query.filter_by(folder=method_name).first()
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage='/static/'+method.folder+'/download.png',
                    def_threshold='',
                    def_style_button='hidden',
                    styleb1='display:none;',
                    styleb2='',
    )

@app.route('/sendfilemethod1',methods=['POST'])
def method1post():
    method_name='method1'
    tval = request.form.get('tval')
    uploaded_file = request.files['image_uploaded']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        filename = uuid.uuid4().hex
        path_img='static/'+method_name+'/temp/'+filename+file_ext
        uploaded_file.save(path_img)
        session['m1']={"path":path_img,"tval":tval}
        new_image = Method1(image=path_img,text=tval)
        db.session.add(new_image)
        db.session.commit()
    # add the new user to the databa
    path='/methods/'+method_name+'.html'
    method=Methods.query.filter_by(folder=method_name).first()
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_threshold=tval,
                    def_style_button='visible',
                    styleb1='display:none;',
                    styleb2=''
    )

@app.route('/calculate',methods=['GET','POST'])
def calc_method1():
    method_name='method1'
    path='/methods/'+method_name+'.html'
    path_img=session['m1']['path']
    tval=session['m1']['tval']
    print('>>PATHOMG>>',path_img)
    print('>>TVAL>>',tval)
    import sys
    #sys.path.append('static/method1')
    from fractal1 import main_fractal
    save_path='static/'+method_name+'/temp/results/'
    name_result=uuid.uuid4().hex
    job = queue.enqueue(main_fractal, path_img,save_path+name_result,int(tval))
    while job.result==None:
        pass
    #img,out=main_fractal(path_img,save_path+name_result,int(tval))
    print ("JOB results>>>",job.result)
    name=os.path.splitext(path_img)[0]
    img,out=job.result
    print('>>out>>',img)
    print('>>text>>',out)
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_threshold=tval,
                    def_style_button='visible',
                    styleb1='',
                    styleb2='display:none;',
                    graph_ready=img+'.png',
                    textdes=out,
                    imgred=img+'result_of_fractal_pores.jpg',

    )
# Method 2
@app.route('/sendfilemethod2',methods=['POST'])
def method2post():
    method_name='method2'
    uploaded_file = request.files['image_uploaded']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        filename = uuid.uuid4().hex
        path_img='static/'+method_name+'/temp/'+filename+file_ext
        uploaded_file.save(path_img)
        session['m2']={"path":path_img}
        #new_image = Method1(image=path_img,text=tval)
        #db.session.add(new_image)
        #db.session.commit()
    # add the new user to the databa
    path='/methods/'+method_name+'.html'
    #method=Methods.query.filter_by(folder=method_name).first()
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_style_button='visible',
                    styleb1='display:none;',
                    styleb2=''
    )
@app.route('/calculatem2',methods=['GET','POST'])
def calc_method2():
    method_name='method2'
    path='/methods/'+method_name+'.html'
    path_img=session['m2']['path']
    print('>>PATHOMG>>',path_img)
    import sys
    #sys.path.append('static/method1')
    from cvmethods import fourier
    save_path='static/'+method_name+'/temp/results/'+os.path.basename(path_img)

    #name_result=uuid.uuid4().hex
    #print("path_img",path_img,"save+name",save_path+name_result)
    job = queue.enqueue(fourier, path_img,save_path)
    while job.result==None:
        pass
    #img,out=main_fractal(path_img,save_path+name_result,int(tval))
    print ("JOB results>>>",job.result)
    name=os.path.splitext(path_img)[0]

    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_style_button='visible',
                    styleb1='',
                    styleb2='display:none;',
                    graph_ready=save_path,



    )
# Method 3
@app.route('/sendfilemethod3',methods=['POST'])
def method3post():
    method_name='method3'
    uploaded_file = request.files['image_uploaded']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        filename = uuid.uuid4().hex
        path_img='static/'+method_name+'/temp/'+filename+file_ext
        uploaded_file.save(path_img)
        session['m3']={"path":path_img}
        #new_image = Method1(image=path_img,text=tval)
        #db.session.add(new_image)
        #db.session.commit()
    # add the new user to the databa
    path='/methods/'+method_name+'.html'
    #method=Methods.query.filter_by(folder=method_name).first()
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_style_button='visible',
                    styleb1='display:none;',
                    styleb2=''
    )
@app.route('/calculatem3',methods=['GET','POST'])
def calc_method3():
    method_name='method3'
    path='/methods/'+method_name+'.html'
    path_img=session['m3']['path']
    print('>>PATHOMG>>',path_img)
    import sys
    #sys.path.append('static/method1')
    from cvmethods import pca_im
    save_path='static/'+method_name+'/temp/results/'+os.path.basename(path_img)

    #name_result=uuid.uuid4().hex
    #print("path_img",path_img,"save+name",save_path+name_result)
    job = queue.enqueue(pca_im, path_img,save_path)
    while job.result==None:
        pass
    #img,out=main_fractal(path_img,save_path+name_result,int(tval))
    print ("JOB results>>>",job.result)
    name=os.path.splitext(path_img)[0]
    name_graph,path_out=job.result
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=path_img,
                    def_style_button='visible',
                    styleb1='',
                    styleb2='display:none;',
                    graph_ready=name_graph,
                    rec_im=path_out,



    )
@app.route('/sendfilemethod4',methods=['GET','POST'])
def calc_method4():
    method_name='method4'
    img='static/'+method_name+'/pat4.jpg'
    img2='static/'+method_name+'/result.jpg'
    #name_result=uuid.uuid4().hex
    #print("path_img",path_img,"save+name",save_path+name_result)
    path='/methods/'+method_name+'.html'
    from cvmethods import structure
    job = queue.enqueue(structure, img,img2)
    while job.result==None:
        pass
    #img,out=main_fractal(path_img,save_path+name_result,int(tval))
    print ("JOB results>>>",job.result)
    df,AxsNC,s_=job.result
    return render_template(path,
                    method=Methods.query.filter_by(folder=method_name).first(),
                    defaultimage=img,
                    def_style_button='visible',
                    styleb1='',
                    styleb2='display:none;',
                    graph_ready=img2,
                    tables=[df.to_html(classes='data')], titles=df.columns.values,
                    text_A=AxsNC,
                    text_s=s_,



    )
