from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            value = Mutable.coerce(key, value)

        return value

    def __setitem__(self, key, value):
        old_value = list.__getitem__(self, key)
        for obj, key in self._parents.items():
            old_value._parents.pop(obj, None)

        list.__setitem__(self, key, value)
        for obj, key in self._parents.items():
            value._parents[obj] = key

        self.changed()

    def __getitem__(self, key):
        value = list.__getitem__(self, key)

        for obj, key in self._parents.items():
            value._parents[obj] = key

        return value

    def __getstate__(self):
        return list(self)

    def __setstate__(self, state):
        self[:] = state
