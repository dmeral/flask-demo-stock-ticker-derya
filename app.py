from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bokeh.plotting import figure
from bokeh.embed import components 
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.io import output_file, output_notebook, show

app = Flask(__name__)

app.vars = {}

def create_plot(stock,types_list):
  # Load data:
  api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=N_mE5xwVmBJ4hfvDMbsP' % stock
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)
  
  # Clean data:
  json_string = json.dumps(raw_data.json(), sort_keys=True)
  obj = json.loads(json_string)
  index_dates = pd.to_datetime(pd.Series(np.array(obj['data'])[:,0]),format="%Y-%m-%d")
  df = pd.DataFrame(np.array(obj['data'])[:,1:],dtype=float,columns=obj['column_names'][1:],index=index_dates)
  
  #print(df)
  # Create the plot:
  plot = figure(title='Data from Quandle WIKI set',
                x_axis_label='date',
                x_axis_type='datetime',
                y_axis_label='stock value')
  colors = ["red","blue","black","magenta"]
  i=0
  for sel in types_list:
    plot.line(df.index,df[sel],color=colors[i],alpha=1.,
               muted_color=colors[i], muted_alpha=0.2,legend=sel)
    i+=1
  plot.legend.location = "top_left"
  plot.legend.click_policy="mute"
  return plot


@app.route('/index',methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index_mine.html')
  else:
    #request was a POST
    app.vars['stock'] = json.loads(json.dumps(request.form['stock_name']))
    types_list = []
    try:
      app.vars['choice1'] = request.form['var1']
      types_list.append(json.loads(json.dumps(request.form['var1'])))
    except:
      pass
    try:
      app.vars['choice2'] = request.form['var2']
      types_list.append(json.loads(json.dumps(request.form['var2'])))
    except:
      pass
    try:
      app.vars['choice3'] = request.form['var3']
      types_list.append(json.loads(json.dumps(request.form['var3'])))
    except:
      pass
    try:
      app.vars['choice4'] = request.form['var4']
      types_list.append(json.loads(json.dumps(request.form['var4'])))
    except:
      pass
    app.vars['types']=types_list
    f = open('output.txt','w')
    f.write('Stock: %s\n'%(app.vars['stock']))
    try:
      f.write('Choice1: %s\n\n'%(app.vars['choice1']))
    except:
      pass
    try:
      f.write('Choice2: %s\n\n'%(app.vars['choice2']))
    except:
      pass
    try:
      f.write('Choice3: %s\n\n'%(app.vars['choice3']))
    except:
      pass
    try:
      f.write('Choice4: %s\n\n'%(app.vars['choice4']))
    except:
      pass
    f.close()
    plot = create_plot(app.vars['stock'],types_list)
    script, div = components(plot)
    return render_template('graph.html',script=script, div=div)
    #variables = json.dumps(app.vars)
    #session['variables'] = variables
    #return redirect(url_for('about', keys='stock',types='blah'))
    



#@app.route('/about',methods=['GET','POST'])
#def about(keys,types):
#  return str(request.args.get('keys'))
#  stock = json.loads(request.args.get('stock_name'))
#  #stock = request.args.get('stock_name')
#  #types = request.args.get('types')
#  return str(stock)
#  #plot = create_plot(app.vars['stock'],types_list)
#  #script, div = components(plot)
#  #return render_template('graph.html',script=script, div=div)


if __name__ == '__main__':
  #app.run(debug=True)
  app.run(port=33507,host='0.0.0.0',debug=True)
