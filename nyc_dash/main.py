
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column
import pandas as pd
#from bokeh.io import curdoc

#load data
df=pd.read_csv('zipaverages.csv')
averagedf=df.groupby('month')['response'].mean().to_frame(name='response').reset_index()

#generate plots
p = figure (plot_width=400, plot_height=400, y_axis_type="linear",x_axis_type='datetime', title="Montlhy distribution of response time to 311 complaints in 2020")
p.xaxis.axis_label = 'Months'
p.yaxis.axis_label = 'Average response time(in hours)'

def getsource (zip):
	return df[df.zip== zip]
zip1 = ColumnDataSource(getsource(10000))
zip2= ColumnDataSource(getsource(10001))


p.line(averagedf['month'], averagedf['response'], legend_label='all', line_color='green', line_width=3)
p.line(x='month', y='response', source=zip1, legend_label='zip1',line_color='purple', line_width = 3)
p.line(x='month', y='response', source=zip2, legend_label='zip2',line_color='blue', line_width = 3)


p.xaxis.ticker = [1, 2, 3, 4, 5, 6, 7, 8, 9]
p.xaxis.major_label_overrides = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May',6:'June', 7:'July', 8:'Aug', 9:'Sept'}


#handle callbacks


def callback1(attr,old, new):
	new_zip=int(d1.value)
	zip1.data = getsource(new_zip)
def callback2(attr,old, new):
	new_zip=int(d2.value)
	zip2.data = getsource(new_zip)

#user interaction
d1 = Select(title = 'zip1', options=df.zip.drop_duplicates().astype(str).to_list(), value='10000')
d2 = Select(title='zip2', options = df.zip.drop_duplicates().astype(str).to_list(), value='10001')
d1.on_change('value', callback1)
d2.on_change('value', callback2)

layout=column(d1, d2, p)
curdoc().add_root(layout)

