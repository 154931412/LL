import json
from datetime import datetime

data = {"now": datetime.now()}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        '''
        如果对象是 datetime 的实例，将其转换为 ISO 格式字符串。否则，使用父类的默认行为。
        :param self: DateTimeEncoder 类的实例。
        :param o: 要序列化的对象。
        :return: 对象的 JSON 可序列化表示。
        '''
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

s = json.dumps(data, cls=DateTimeEncoder)
print(s)
print(json.loads(s)["now"])