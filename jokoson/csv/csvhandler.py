import csv
import inspect
from io import StringIO

from jokoson.db import models

from jokoson.csv import parser

class CSVHandler(object):

    def __init__(self, viewset, fd):
        self.viewset = viewset
        self.fd = fd

    def csv_import(self):
        mapper = parser.MapperParser('mapper.yaml').get_mapper()

        with self.fd as stream:
            csvf = StringIO(stream.read().decode())
            reader = csv.DictReader(csvf, delimiter=',')

            for row in reader:
                for table in mapper:
                    for name, property_map in table.items():
                        properties = self._build_properties(property_map, row)
                        data = {'data': properties}
                        viewset = self.viewset.get_viewset(name)
                        serializer = viewset.get_serializer_class()(**data)

                        try:
                            serializer.validate(properties)
                            serializer.instance_query()
                        except Exception as ex:
                            continue

                        serializer.is_valid()
                        viewset.perform_create(serializer)
                        vv = viewset.queryset.values()

    def _build_properties(self, property_map, properties):
        property_dict = dict()
        for key, value in properties.items():
            update_key = key.strip()
            for k, v in property_map.items():
                if update_key == v:
                    property_dict[k] = value

        return property_dict

    def csv_export(self):
        pass

    def download(self):
        pass

    def upload(self):
        pass

if __name__ == "__main__":
    handler = CSVHandler()

    filename = '/home/stack/jokoson/jokoson/csv/summary.csv'
    fd = open(filename, 'r')
    handler.csv_import(fd)