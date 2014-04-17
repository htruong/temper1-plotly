import plotly
import datetime
import time
import numpy as np
import json
import time

from subprocess import Popen, PIPE

# Fill in the config.json file in this directory with your plotly username, 
# plotly API key, and your generated plotly streaming tokens
# Sign up to plotly here: https://plot.ly/ssu
# View your API key and streaming tokens here: https://plot.ly/settings

with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

username = plotly_user_config['plotly_username'] 
api_key = plotly_user_config['plotly_api_key']
stream_token = plotly_user_config['plotly_streaming_tokens']



# Initialize your plotly object
p = plotly.plotly(username, api_key)


# Initialize your plotly real-time streaming graph with a REST API call
# Embed the stream token in one of the traces of a plotly-data object - one token per trace
# Also embed 'maxpoints', the number of points that you want plotted at a time

# The `iplot` command will embed our plotly graph as an iframe in this notebook
# Each plotly graph has a unique url that you can share and anyone can view 
# your streaming graph in real-time
p.iplot([{'x': [], 'y': [], 'type': 'scatter', 'mode': 'lines',
            'stream': {'token': stream_token, 'maxpoints': 3600}
          }],
        filename='Is-Jimmies-Cold', fileopt='extend')


# Now stream! Write to a plotly stream object
# Our data will be in the the form:
# {'x': x_data, 'y':y_data}
# Each point that we yield will get shipped through plotly's servers
# to the graph your web-browser, updating it in real-time

s = plotly.stream(stream_token)
i=0

while True:
    i+=1

    (stdout, stderr) = Popen(["./get-temp.sh"], stdout=PIPE).communicate()
    # log current time and a random number
    x_data_point = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    y_data_point = stdout
    print('Sending...', 'x',x_data_point,'y',y_data_point)
    s.write({'x': x_data_point, 'y': y_data_point})
    time.sleep(60)

s.close()