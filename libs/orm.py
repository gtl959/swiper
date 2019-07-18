
class ModelToDictMixin():

    def to_dict(self,exclude=None):
        if not exclude:
            exclude = []
        if isinstance(exclude,str):
            exclude = [str]
        fields = self._meta.fields

        dic = {}
        for i in fields:
            key = i.attname
            if key not in exclude:
                value = getattr(self,key)
                dic[key] = value

        return dic
