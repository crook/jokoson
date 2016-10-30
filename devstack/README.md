A simple Rest Demo
# jokoson

Demo site: http://54.238.155.90:8888

Admin site: http://54.238.155.90:8888/admin
user/password: admin/zaq12WSX

REST API endpoint:
http://54.238.155.90:8888/

Example:


# create one category
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"description":"images"}' http://10.110.126.208:8888/categories/
{"id":1,"description":"images"}
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"description":"food"}' http://10.110.126.208:8888/categories/
{"id":2,"description":"food"}
ranc-m01:devstack ranc$ curl http://10.110.126.208:8888/categories/
[{"id":1,"description":"images"},{"id":2,"description":"food"}]


# create one vendor
ranc-m01:~ ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json"  -d '{"name":"EMC", "city":"Shanghai", "cell_phone":"123", "office_phone":"123456", "address1":"addrss1","address2":"address2"}' http://10.110.126.208:8888/vendors/
{"url":"http://10.110.126.208:8888/vendors/2/","name":"EMC","city":"Shanghai","cell_phone":"123","office_phone":"123456","address1":"addrss1","address2":"address2"}

# create one equip
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"sn":"XXXX", "model":"model", "description":"dddd", "vendor_id":"1", "category_id":"1"}' http://10.110.126.208:8888/equips/
{"id":1,"category_id":"1","vendor_id":"1","created_date":"2016-10-30T12:38:57.852857Z","updated_date":"2016-10-30T12:38:57.852899Z","sn":"XXXX","model":"model","public":false,"description":"dddd","vendor":{"id":1,"name":"EMC","city":"Shanghai","cell_phone":"123","office_phone":"123456","address1":"addrss1","address2":"address2"},"category":{"id":1,"description":"images"}}
# Update
ranc-m01:devstack ranc$ curl -X PUT -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"sn":"XXXX", "model":"model", "description":"dddd", "vendor_id":"1", "category_id":"2"}' http://10.110.126.208:8888/equips/1/
{"id":1,"category_id":"2","vendor_id":"1","created_date":"2016-10-30T12:38:57.852857Z","updated_date":"2016-10-30T12:40:02.236397Z","sn":"XXXX","model":"model","public":false,"description":"dddd","vendor":{"id":1,"name":"EMC","city":"Shanghai","cell_phone":"123","office_phone":"123456","address1":"addrss1","address2":"address2"},"category":{"id":2,"description":"goods"}}

# create one order
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"starttime":"2016-01-01T12:00:30","endtime":"2016-05-30T12:00:40","duration":"200","money":"1001.001","equip_id":"2"}'  http://10.110.126.208:8888/orders/
{"id":1,"equip_id":"2","buyer":"http://10.110.126.208:8888/users/1/","signtime":"2016-10-30T12:44:08.231065Z","starttime":"2016-01-01T12:00:30Z","endtime":"2016-05-30T12:00:40Z","duration":200,"money":1001.001,"valid":true,"equip":{"id":2,"created_date":"2016-10-30T12:42:26.555498Z","updated_date":"2016-10-30T12:42:26.555535Z","sn":"XXXX","model":"model","public":false,"description":"dddd","vendor":1,"category":1}}


# create one GPSsensor
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"vendor_id":"1", "model":"helloModel","status":"6", "batterypercent":"50", "equip_id":"1", "category_id":"2"}' http://10.110.126.208:8888/gpssensors/
{"id":1,"equip_id":"1","category_id":"2","vendor_id":"1","gpsdatas":[],"status":6,"model":"helloModel","batterypercent":50,"equip":{"id":1,"created_date":"2016-10-30T12:38:57.852857Z","updated_date":"2016-10-30T12:40:02.236397Z","sn":"XXXX","model":"model","public":false,"description":"dddd","vendor":1,"category":2},"vendor":{"id":1,"name":"EMC","city":"Shanghai","cell_phone":"123","office_phone":"123456","address1":"addrss1","address2":"address2"},"category":{"id":2,"description":"goods"}}


# create one GPSdata
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"time":"2016-01-11T12:12:12","x":"60.12","y":"120.86", "height":"100", "sensor_id":"1"}' http://10.110.126.208:8888/gpsdatas/
{"id":1,"sensor_id":"1","time":"2016-01-11T12:12:12Z","x":60.12,"y":120.86,"height":100.0,"sensor":{"id":1,"status":6,"model":"helloModel","batterypercent":50,"equip":1,"vendor":1,"category":2}}


