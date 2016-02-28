from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():

  TOOLS = 'box_zoom,box_select,crosshair,resize,reset'
  plot = figure(tools=TOOLS, width=450, height=450)
  plot.circle([1,2], [3,4])
  script, div = components(plot)
  print div
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
