from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bokeh.plotting import figure
from bokeh.embed import components 
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.io import output_file, output_notebook, show
import os

quandl = os.environ['QUANDL_KEY']
print(quandl)

app = Flask(__name__)

def create_plot(stock,types_list):
  # Load data:
  api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key' % stock + str(quandl)
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


@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index_mine.html')


@app.route('/about',methods=['GET','POST'])
def about():
  if request.method == 'POST':
    stock = request.form['stock_name']
    variables = ['var1','var2','var3','var4']
    options = []
    for var in variables:
      try:
        options.append(request.form[var])
      except:
        pass
    plot = create_plot(stock,options)
    script, div = components(plot)
    return render_template('graph.html',script=script, div=div)


if __name__ == '__main__':
  app.run(debug=True)
  #app.run(port=33507,host='0.0.0.0',debug=False)
