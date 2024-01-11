#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
from flask import Flask
from gevent import pywsgi
from flask import request, render_template
import pickle
app=Flask(__name__)
modelph=pickle.load(open('modelph.sav','rb'))
modeltn=pickle.load(open('modeltn.sav','rb'))
modeltoc=pickle.load(open('modeltoc.sav','rb'))
modeltp=pickle.load(open('modeltp.sav','rb'))
@app.route('/')
def home():
   
    return render_template('page.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    C=float(request.form['carbon'])
    H=float(request.form['hydrogen'])
    O=float(request.form['oxygen'])
    S=float(request.form['sulfur'])
    N=float(request.form['nitrogen'])
    A=float(request.form['ash'])
    P=float(request.form['protein'])
    L=float(request.form['lipid'])
    Car=float(request.form['carbohydrate'])
    T=float(request.form['temperature'])
    RT=float(request.form['residence time'])
    SC=float(request.form['solid content'])
    x=[C,H,O,S,N,A,P,L,Car,T,RT,SC]
    x=np.array(x).reshape(1,12)
    y_predict1=modelph.predict(x)[0]
    pH=np.round(y_predict1,2)
    y_predict2=modeltn.predict(x)[0]
    TN=np.round(y_predict2,2)
    y_predict3=modeltoc.predict(x)[0]
    TOC=np.round(y_predict3,2)
    y_predict4=modeltp.predict(x)[0]
    TP=np.round(y_predict4,2)
    return render_template('page.html',Predicted_pH='{}'.format(pH),Predicted_TN='{}'.format(TN),Predicted_TOC='{}'.format(TOC),Predicted_TP='{}'.format(TP))


if __name__=='__main__':
    app.run(debug=True,port=5500,use_reloader=False)



# %%
