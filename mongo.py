def match(doc, _filter):
    if _filter:
        return all([doc.get(k) == v for k, v in _filter.items()])
    return True


class MockMongoClient:
    def __init__(self, uri):
        self.db = MockDatabase()
        self.uri = uri

    def get_default_database(self):
        return self.db


class MockCollection:
    def __init__(self, data=None):
        self.data = [] if data is None else data

    def find_one(self, _filter=None):
        return next((e for e in self.data if match(e, _filter)), None)

    def find(self, _filter=None):
        return [e for e in self.data if match(e, _filter)]

    def insert_one(self, doc):
        self.data.append(doc)

    def insert_many(self, docs):
        self.data.extend(docs)

    def replace_one(self, old, new):
        e = self.find_one(old)
        if e:
            self.data.remove(e)
        self.data.append(new)

    def delete_one(self, _filter):
        e = self.find_one(_filter)
        if e:
            self.data.remove(e)

    def count(self, _filter=None):
        return len(self.find(_filter))


class MockSystemCollection(MockCollection):
    def __init__(self, data=None):
        super().__init__(data)
        self.views = MockCollection()


class MockDatabase:
    def __init__(self):
        self.gid = MockGidCollection()
        self.system = MockSystemCollection()


class MockGidCollection(MockCollection):
    def __init__(self, data=None):
        super().__init__(data or [
            {'gid': 1, 'gmachine_id': '1', 'hostname': 'host1', 'version': 9,
             'current': 'True'},
            {'gid': 2, 'gmachine_id': '2', 'hostname': 'host2', 'version': 9},
            {'gid': 3, 'gmachine_id': '2', 'hostname': 'host2', 'version': 10,
             'current': True},
            {'gid': 4, 'gmachine_id': '3', 'current': True},
            {'gid': 5, 'gmachine_id': '4', 'version': 10, 'current': True}
        ])
