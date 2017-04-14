import csv
from io import StringIO
from jokoson.csv.parser import MapperParser


class CSVHandler(object):
    def __init__(self, viewset, fd=None):
        self.viewset = viewset
        self.fd = fd

    def csv_import(self):
        mapper, table_header = MapperParser('mapper.yaml').get_mapper()

        with self.fd as stream:
            csvf = StringIO(stream.read().decode())
            reader = csv.DictReader(csvf, delimiter=',')

            for row in reader:
                for model in mapper:
                    for model_name, prop_map in model.items():
                        properties = self.get_model_props(row, prop_map)

                        # FIXME: When upload CSV file, only support one equip for each order
                        # Convert the equip sn into one list for later query
                        if model_name == 'Order':
                            properties['equips'] = [properties['equips']]

                        data = {'data': properties}
                        viewset = self.viewset.get_viewset(model_name)
                        serializer = viewset.get_serializer_class()(**data)

                        try:
                            # serializer.validate(properties)
                            serializer.instance_query()
                            serializer.is_valid(raise_exception=True)
                        except Exception:
                            continue

                        viewset.perform_create(serializer)

    def get_model_props(self, content, prop_map):
        property_dict = dict()

        for k, v in prop_map.items():
            property_dict[v] = content[k].strip() if k in content else None

        return property_dict

    def csv_export(self):

        mapper, table_header = MapperParser('mapper.yaml').get_mapper()
        export_dict = {
            'header': table_header,
            'content': [],
        }
        mapper.reverse()
        for model in mapper:
            for model_name, prop_map in model.items():
                viewset = self.viewset.get_viewset(model_name)
                serializer = viewset.get_serializer_class()(viewset.queryset,
                                                            many=True)
                for data in serializer.data:
                    serializer.child.export(data, mapper, export_dict)

        return export_dict

    def download(self):
        pass

    def upload(self):
        pass
