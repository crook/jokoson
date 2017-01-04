import csv
from io import StringIO
from jokoson.csv.parser import MapperParser


class CSVHandler(object):
    def __init__(self, viewset, fd):
        self.viewset = viewset
        self.fd = fd

    def csv_import(self):
        mapper = MapperParser('mapper.yaml').get_mapper()

        with self.fd as stream:
            csvf = StringIO(stream.read().decode())
            reader = csv.DictReader(csvf, delimiter=',')

            for row in reader:
                for model in mapper:
                    for model_name, prop_map in model.items():
                        properties = self.get_model_props(row, prop_map)
                        data = {'data': properties}
                        viewset = self.viewset.get_viewset(model_name)
                        serializer = viewset.get_serializer_class()(**data)

                        try:
                            # serializer.validate(properties)
                            serializer.instance_query()
                            serializer.is_valid()
                        except Exception:
                            continue

                        viewset.perform_create(serializer)

    def get_model_props(self, content, prop_map):
        property_dict = dict()

        for k, v in prop_map.items():
            property_dict[v] = content[k].strip() if k in content else None

        return property_dict

    def csv_export(self):
        pass

    def download(self):
        pass

    def upload(self):
        pass
