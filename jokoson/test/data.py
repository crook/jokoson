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

    category = {
        'star-8': {
            'name': 'star-8',
            'description': 'This is a star-8!',
        },
        'star-10': {
            'name': 'star-10',
            'description': 'This is a star-10!',
        },
    }

    vendor = {
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
        }
    }

    equip = {
        'star-10-1111111': {
            'sn': 'star-10-1111111',
            'model': 'star-10',
            'status': 1,
            'health': 1,
            'description': 'This is a star-10-1111111!',
            'vendor': vendor['Hako']['name'],
            'category': category['star-10']['name'],
            'gps_status': 1,
            'gps_model': 'gps_model-1',
            'gps_batterypercent': 60,
            'gps_time': '2016-10-30T12:38:57Z',
            'x': 60.12,
            "y": 120.86,
            "z": 120.86,
        },
        'star-10-2222222': {
            'sn': 'star-10-2222222',
            'model': 'star-10',
            'status': 1,
            'health': 2,
            'description': 'This is a star-10-1111111!',
            'vendor': vendor['Hako']['name'],
            'category': category['star-10']['name'],
            'gps_status': 1,
            'gps_model': 'gps_model-2',
            'gps_batterypercent': 70,
            'gps_time': '2017-10-30T12:38:57Z',
            'x': 70.12,
            "y": 130.86,
            "z": 130.86,
        },
    }

    orders = {
        'star-10-1111111': {
            'equip_sn': equip['star-10-1111111']['sn'],
            'starttime':'2017-10-30T12:38:57Z',
            'endtime':'2018-10-30T12:38:57Z',
            'total_cost': 9000.00,
            'valid': True,
            'duration': '365 00:00:00',
            'tenant': None,
        },
        'star-10-2222222': {
            'equip_sn': equip['star-10-1111111']['sn'],
            'starttime':'2017-10-30T12:38:57Z',
            'endtime':'2018-10-30T12:38:57Z',
            'total_cost': 10000.00,
            'valid': True,
            'duration': '365 00:00:00',
            'tenant': None,
        },
    }


