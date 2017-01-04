class TestData(object):
    user = {
        'john': {
            'username': 'john',
            'password': 'johnpassword',
            'first_name': 'John',
            'last_name': 'Handsome',
            'email': 'john.handsome@google.com',
            'is_active': True,
        },
        'mike': {
            'username': 'mike',
            'password': 'tysonpassword',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'email': 'mike.tyson@google.com',
            'is_active': True,
        },
    }

    manufacture = {
        'Hako': {
            'name': 'Hako',
            'city': 'Bad Oldesloe',
            'cell_phone': '0049-4531-806-0',
            'office_phone': '0049-4531-806-0',
            'address': 'Hamburger Straße 209-239',
        },
        'Karcher': {
            'name': 'Karcher',
            'city': 'Winnenden',
            'cell_phone': '+49 (0) 7195 / 14-0',
            'office_phone': '+49 (0) 7195 / 14-0',
            'address': 'Alfred-Kärcher-Strasse 28-40 ',
        },
        'Haulotte': {
            "name": "Haulotte",
            "city": "Virginia",
            "cell_phone": "",
            "office_phone": "(001)757-689-2146",
            "address": "3409 Chandler Creek Rd. Virginia Beach VA 23453 United States"
        }

    }

    model = {
        'star-8': {
            'name': 'star-8',
            'description': 'This is a star-8!',
            'manufacture': manufacture['Haulotte']['name'],
        },
        'star-10': {
            'name': 'star-10',
            'description': 'This is a star-10!',
            'manufacture': manufacture['Haulotte']['name'],
        },
    }

    equip = {
        'ME 112104': {
            'sn': 'ME 112104',
            'description': 'This is ME 112104!',
            'manufacture': manufacture['Haulotte']['name'],
            'model': model['star-10']['name'],
            'status': 0,
            'health': 'OK',
            'gps_status': 1,
            'gps_model': 'gps_model-1',
            'gps_batterypercent': 60,
            'gps_time': '2016-10-30T12:38:57Z',
            'x': 60.12,
            "y": 120.86,
            "z": 120.86,
        },
        'ME 111501': {
            'sn': 'ME 111501',
            'description': 'This is ME 111501!',
            'manufacture': manufacture['Haulotte']['name'],
            'model': model['star-10']['name'],
            'status': 0,
            'health': 'BAD',
            'gps_status': None,
            'gps_model': None,
            'gps_batterypercent': None,
            'gps_time': None,
            'x': None,
            "y": None,
            "z": None,
        },
    }
    orders = {
        'ME 112104': {
            'tenant': None,
            'equip': equip['ME 112104']['sn'],
            'starttime': '2017-10-30T12:38:57Z',
            'endtime': '2018-10-30T12:38:57Z',
            'total_cost': 9000.00,
            'valid': True,
            'duration': '365 00:00:00',

        },
        'ME 111501': {
            'tenant': None,
            'equip': equip['ME 111501']['sn'],
            'starttime': '2017-10-30T12:38:57Z',
            'endtime': '2018-10-30T12:38:57Z',
            'total_cost': 10000.00,
            'valid': True,
            'duration': '365 00:00:00',
        },
    }
