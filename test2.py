import datetime
time = '2021-11-13 23:03:52.608320+00:00'
print(datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ'))