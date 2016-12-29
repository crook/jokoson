import inspect
import os
import yaml


class MapperParser(object):
    def __init__(self, file_name):
        self.file_name = file_name

    @classmethod
    def _get_directory(cls):
        return os.path.dirname(inspect.getfile(cls))

    def _read(self):
        filename = os.path.realpath(
            os.path.join(self._get_directory(), self.file_name))
        with open(filename, 'r') as stream:
            ret = yaml.load(stream)

        return ret

    def get_mapper(self):
        mapper = self._read()
        obj_list = []
        for item in mapper['CVS_Mapper']:
            prop = dict()
            for properties in item['properties']:
                for key, value in properties.items():
                    prop[key] = value
            obj_list.append({item['obj_name']: prop})

        return obj_list


if __name__ == "__main__":
    parser = MapperParser('mapper.yaml')
    print(parser.get_mapper())
