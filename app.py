from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':

    # get stock data from quandl
    ticker=request.form['ticker']
    api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.csv?column_index=4&exclude_column_names&&order=asc' %ticker
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    rtext=str(raw_data.text).split('\n')[:-1]
    data=zip(*[line.split(',') for line in rtext])

    # put into a pandas dataframe
    df=pd.DataFrame({'date':pd.to_datetime(data[0]),'price':pd.to_numeric(data[1])})
    df['price']=df['price'].astype('float')

    # plot with bokeh
    plot = figure(width=450, height=450, y_axis_label='Stock Price', x_axis_label='date', x_axis_type='datetime')
    plot.line(df['date'],df['price'],color='green',line_width=3)

    script, div = components(plot)
    return render_template('graph.html', ticker=ticker, script=script, div=div)

  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
#  app.run(debug=True)
