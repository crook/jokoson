A simple Rest Demo
# jokoson

Demo site: http://54.238.155.90:8888

Admin site: http://54.238.155.90:8888/admin
user/password: admin/zaq12WSX

REST API endpoint:
http://54.238.155.90:8888/

Example:
# create one vendor
ranc-m01:~ ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json"  -d '{"name":"EMC", "city":"Shanghai", "cell_phone":"123", "office_phone":"123456", "address1":"addrss1","address2":"address2"}' http://10.110.126.208:8888/vendors/
{"url":"http://10.110.126.208:8888/vendors/2/","name":"EMC","city":"Shanghai","cell_phone":"123","office_phone":"123456","address1":"addrss1","address2":"address2"}

# create one equip
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"sn":"XXXX", "model":"model", "description":"dddd", "vendor_id":"1", "category_id":"1"}' http://10.110.126.208:8888/equips/
{"url":null,"category":"Category object","vendor":"Vendor object","created_date":null,"updated_date":null,"sn":"XXXX","model":"model","public":false,"description":"dddd"}

# create one order
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"starttime":"2016-01-01T12:00:30","endtime":"2016-05-30T12:00:40","duration":"200","money":"1001.001","equip_id":"1"}'  http://10.110.126.208:8888/orders/
{"url":"http://10.110.126.208:8888/orders/2/","equip":"Equip object","buyer":"http://10.110.126.208:8888/users/1/","signtime":"2016-10-30T03:41:39.222659Z","starttime":"2016-01-01T12:00:30Z","endtime":"2016-05-30T12:00:40Z","duration":200,"money":1001.001,"valid":true}

# create one GPSsensor
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"vendor":"2", "model":"helloModel","status":"6", "batterypercent":"50", "equip_id":"1", "category_id":"2"}' http://10.110.126.208:8888/gpssensors/
{"url":"http://10.110.126.208:8888/gpssensors/1/","equip":"Equip object","category":"Category object","vendor":"Vendor object","gpsdatas":[],"status":6,"model":"helloModel","batterypercent":50}

# create one GPSdata
ranc-m01:devstack ranc$ curl -X POST -u admin:zaq12WSX  -H "Content-Type: application/json" -d '{"time":"2016-01-11T12:12:12","x":"60.12","y":"120.86", "height":"100", "sensor_id":"1"}' http://10.110.126.208:8888/gpsdatas/
{"url":"http://10.110.126.208:8888/gpsdatas/1/","sensor":"Gpssensor object","time":"2016-01-11T12:12:12Z","x":60.12,"y":120.86,"height":100.0}



