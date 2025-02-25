from datetime import datetime, date, time
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware

from tinydb_serialization.serializers import DateTimeSerializer

class DateSerializer(Serializer):
    # The class this serializer handles --> must be date instead of datetime.date
    OBJ_CLASS = date

    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return date.fromisoformat(s)

class TimeSerializer(Serializer):
    # The class this serializer handles --> must be time instead of datetime.time
    OBJ_CLASS = time
    
    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return time.fromisoformat(s)

serializer = SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')
serializer.register_serializer(DateSerializer(), 'TinyDate')
serializer.register_serializer(TimeSerializer(), 'TinyTime')