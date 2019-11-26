import datetime as dt
import json
import plotly.figure_factory as ff

today = dt.datetime.now()
today_str = today.strftime('%Y-%m-%d')
j = json.loads(open('timeline.dev').read())
EvtLst = []


for x in range(len(j['TimeLineHandlers'])):
    EvtType = j['TimeLineHandlers'][x]['HandlerType']
    EvtStart = "{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOn'])
    EvtEnd = "{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOff'])
    Evt = dict(Task = EvtType, Start = EvtStart, Finish = EvtEnd, Resource = EvtType)
    EvtLst.append(Evt)

colors = dict(BrowserChrome = 'rgb(0, 255, 0)', 
              BrowserFirefox = 'rgb(0, 225, 0)', 
              BrowserIE = 'rgb(0, 200, 0)', 
              Clicks = 'rgb(255, 0, 0)', 
              Command = 'rgb(225, 0, 0)', 
              Excel = 'rgb(175, 175, 0)', 
              Notepad = 'rgb(200, 200, 0)', 
              Outlook = 'rgb(255, 0, 255)',
              PowerPoint = 'rgb(225, 225, 0)', 
              Reboot = 'rgb(200, 0, 0)', 
              Watcher = 'rgb(175, 0, 0)', 
              Word = 'rgb(255, 255, 0)')

fig = ff.create_gantt(EvtLst, colors=colors, index_col='Resource', show_colorbar = True, group_tasks = True)
fig.show()


#FOO: just to help me remember syntax of stuff
#dir(j)
#j.keys()
#print(j['TimeLineHandlers'][0].keys())
#print(j['TimeLineHandlers'][1]['TimeLineEvents'][0]['CommandArgs'][11])


