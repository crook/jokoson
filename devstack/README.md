A simple Rest Demo
# jokoson

Demo site: http://54.238.155.90:8888

Admin site: http://54.238.155.90:8888/admin
user/password: admin/zaq12WSX

REST API endpoint:
http://54.238.155.90:8888/

Example:

ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX -d "sn=BBBBBBBB&public=true" http://54.238.155.90:8888/devices/
{"id":3,"sn":"BBBBBBBB","public":true,"style":"basic","created_date":"2016-10-23T10:43:42.515593Z","updated_date":"2016-10-23T10:43:42.515634Z","owner":"admin"}

ranc-m01:devstack ranc$ curl -X GET -u admin:zaq12WSX  http://54.238.155.90:8888/devices/
[{"id":1,"sn":"AAAAAAA","public":true,"style":"super","created_date":"2016-10-23T10:15:18.863088Z","updated_date":"2016-10-23T10:15:18.863123Z","owner":"admin"},{"id":2,"sn":"hello","public":false,"style":"basic","created_date":"2016-10-23T10:30:04.468131Z","updated_date":"2016-10-23T10:30:04.468167Z","owner":"admin"},{"id":3,"sn":"BBBBBBBB","public":true,"style":"basic","created_date":"2016-10-23T10:43:42.515593Z","updated_date":"2016-10-23T10:43:42.515634Z","owner":"admin"}]

ranc-m01:devstack ranc$ curl -X GET -u admin:zaq12WSX  http://54.238.155.90:8888/devices/1/
{"id":1,"sn":"AAAAAAA","public":true,"style":"super","created_date":"2016-10-23T10:15:18.863088Z","updated_date":"2016-10-23T10:15:18.863123Z","owner":"admin"}
