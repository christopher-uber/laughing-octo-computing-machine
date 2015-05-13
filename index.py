__author__ = 'Root'
# -*- coding: utf-8 -*-

import datetime
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS


FLOW = OAuth2WebServerFlow(
    client_id='729387081896-fcuv85q1fg17ers4jtshbisc5h40bjge.apps.googleusercontent.com',
    client_secret='v3ISkJXZtvig1F-0cKbMx9OK',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='FamilyCal/v1')
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid is True:
    credentials = run(FLOW, storage)
http = httplib2.Http()
http = credentials.authorize(http)
service = build(serviceName='calendar', version='v3', http=http,
                developerKey='AIzaSyBSeXBYAHbfOTbpa2JnFj4mckqeX6Srb0s')

dinnerstart = datetime.time(18, 00, 0)
dinnerend = datetime.time(19, 00, 0)
eveningstart = datetime.time(19, 30, 0)
eveningend = datetime.time(23, 59, 0)

today2 = datetime.datetime.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

timemin = datetime.datetime(today2.year, today2.month, today2.day, 0, 0, 0).strftime("%Y-%m-%dT%H:%M:%S%z")
timemax = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0).strftime("%Y-%m-%dT%H:%M:%S%z")


def events(calendar, timemin2, timemax2):
    lst = []
    json_obj = service.events().list(calendarId=calendar, orderBy='startTime',
                                     singleEvents="true", timeMax=timemax2 + "+10:00",
                                     timeMin=timemin2 + "+10:00").execute()
    eventlst = json_obj["items"]
    for event in eventlst:
        sum = str(event["summary"])
        starttime = event["start"]["dateTime"]
        endtime = event["end"]["dateTime"]
        loc = event["location"]
        dinner = searchtime(starttime, endtime, dinnerstart, dinnerend)
        evening = searchtime(starttime, endtime, eveningstart, eveningend)
        lst.append({"sum": sum, "start": atomtohourmin(starttime), "end": atomtohourmin(endtime),
                    "loc": loc, "dinner": dinner, "evening": evening})
    return lst


def atomtohourmin(atomstr):
    convert = datetime.datetime.strptime(atomstr[0:19], "%Y-%m-%dT%H:%M:%S")
    return convert.strftime("%H:%M")


def searchtime(atomstart, atomend, start, end):
    convertstart = datetime.datetime.strptime(atomstart[0:19], "%Y-%m-%dT%H:%M:%S")
    convertend = datetime.datetime.strptime(atomend[0:19], "%Y-%m-%dT%H:%M:%S")
    if start <= convertstart.time() <= end:
        return True
    elif start <= convertend.time() <= end:
        return True
    else:
        return False


def daily(time, lst):
    for event in lst:
        if event[time] is True:
            return ""
    return "checked"


def daily2(homeloc, lst):
    for event in lst:
        if event["loc"] is not homeloc:
            return ""
    return "checked"

chrislst = events('opensource25@gmail.com', timemin, timemax)
dadlst = events('kenneth.uber@gmail.com', timemin, timemax)
domlst = events('dominic.uber@gmail.com', timemin, timemax)

today = datetime.datetime.today().strftime("%d %B %y")


def colcontent(name, address, date, eventlst):
    print """
            <div class="ui cards">
            <div class="card">
            <div class="content">
                    <a class="header">{0}</a>
                    <div class="meta">
                    <span class="date">{1}</span>
                </div>
                <div class="description">
                <form class="ui form">
                    <p>
                    <div class="field">
                        <div class="ui toggle checkbox">
                        <input type="checkbox" name="home" {5}>
                        <label>At home</label>
                        </div>
                        </div>
                    </p>
                    <p><div class="field">
                        <div class="ui toggle checkbox">
                        <input type="checkbox" name="dinner" {3}>
                        <label>Dinner</label>
                        </div>
                        </div></p>
                    <p><div class="field">
                        <div class="ui toggle checkbox">
                        <input type="checkbox" name="evening" {4}>
                        <label>Evening</label>
                        </div>
                        </div></p>
                    </form>
                </div>
            </div>
            </div>
            <div class="card">
                <div class="content">
                <div class="header">{2}</div>
                <div class="meta">Calendar</div>
                <div class="description">""".format(name, address, date, daily("dinner", eventlst),
                                                    daily("evening", eventlst), daily2(address, eventlst))
    for event in eventlst:
        print """
                    <table>
                    <tr>
                        <td style='width:200px'>
                    <span aligned='left'>{0}</span> </td>
                        <td>
                        <span aligned='right'> {1} - {2} </span> </td>
                        </tr>
                        </table>
                    <span class='meta'> {3} </span> """.format((event["sum"]),
                                                               event["start"], event["end"], event["loc"])
    print """</div>
                </div>
                </div>
            </div>"""


print "Content-Type: text/html"
print
print """
<!DOCTYPE html>
<html>
<head>
  <!-- Standard Meta -->
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta http-equiv="refresh" content="60">
  <!-- Site Properities -->
  <title>Homepage</title>

    <link rel="stylesheet" type="text/css" href="./Semantic-UI-1.11.6/dist/semantic.css">
  <link rel="stylesheet" type="text/css" href="homepage.css">

  <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.js"></script>
    <script src="./Semantic-UI-1.11.6/dist/semantic.js"></script>
  <script src="homepage.js"></script>

</head>


<body>
<div class="ui inverted masthead segment">
    <div class="ui page grid">
      <div class="column">
<div class="ui inverted blue menu">
          <div class="header item">Dashboard Calendar</div>
          <div class="right menu">
            <a class="item">Weather</a>
            <a class="item">Dinner</a>
          </div>
        </div>
        </div>
        </div>
</div>
  <div class="ui vertical feature segment">
    <div class="ui centered page grid">
      <div class="fourteen wide column">
        <div class="ui three column center aligned stackable divided grid">
          <div class="column">"""
colcontent("Christopher Uber", "104 Middlesex Rd", today, chrislst)
print """
          </div>
          <div class="column">"""
colcontent("Kennth Uber", "104 Middlesex Rd", today, dadlst)
print"""
          </div>
          <div class="column">"""
colcontent("Dominic Uber", "104 Middlesex Rd", today, domlst)
print """
          </div>
          </div>
          </div>
          </div>

</body>
</html>"""