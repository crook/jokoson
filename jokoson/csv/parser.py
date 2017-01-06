import inspect
import pprint
from datetime import datetime

import os
import yaml


class MapperParser(object):
    def __init__(self, file_name):
        self.file_name = file_name

    @classmethod
    def _get_directory(cls):
        return os.path.dirname(inspect.getfile(cls))

    def read(self):
        filename = os.path.realpath(
            os.path.join(self._get_directory(), self.file_name))
        with open(filename, 'r') as stream:
            ret = yaml.load(stream)

        return ret['import'], ret['export']

    def get_mapper(self):
        mapper, table_header = self.read()
        mapper.sort(key=lambda model: model['order'])
        ordered_model = []
        for item in mapper:
            prop = dict()
            for props in item['properties']:
                for key, value in props.items():
                    prop[value] = key
            ordered_model.append({item['name']: prop})

        return ordered_model, table_header


if __name__ == "__main__":
    parser = MapperParser('mapper.yaml')
    pprint.pprint(parser.get_mapper())

    t_start = datetime('2017-12-29T00:04:07')
    t_end = datetime('2018-12-29T00:04:07')
    duration = datetime.utcfromtimestamp(t_end - t_start)
    print(duration)
