class Criteria(object):
    """
    criteria = Criteria.equal(title='some string')
    repository = Repository()
    objects_list = repository.find_by_criteria(criteria)
    """

    def __init__(self):
        self.operator = None

    @staticmethod
    def equal(**kwargs):
        for k, v in kwargs.items():
            return EqualCriteria('=', k, v)

    @staticmethod
    def between(**kwargs):
        print(kwargs.keys(), flush=True)
        print(kwargs.values(), flush=True)
        b = BetweenCriteria()
        for k, v in kwargs.items():
            if k == 'cond_rhs':
                b.set_rhs_condition(v)
            elif k == 'cond_lhs':
                b.set_lhs_condition(v)
            elif k == 'join':
                b.set_join_function(v)
            else:
                b.add_field_value(k, v)
        return b

    def str(self, data_map):
        pass

    def values(self):
        pass


class EqualCriteria(Criteria):
    def __init__(self, op, field, value):
        super().__init__()
        self.operator = op
        self.field = field
        self.value = value

    def str(self, data_map):
        return '{field}{operator}{value}'.format(field=data_map.field(self.field), operator=self.operator,
                                                 value=self.value)

    def values(self):
        return self.value


class BetweenCriteria(Criteria):
    def __init__(self):
        super().__init__()
        self.join_operator = None
        self.conditions = []

    def str(self, data_map):
        s = '('
        for e in self.conditions:
            s = s + '{f}{op}?'.format(f=data_map.field(e['f']), op=e['op'])
            s = s + ' ' + self.join_operator + ' '
        s = s[:-(len(self.join_operator) + 2)] + ')'
        return s

    def values(self):
        return tuple([e['v'] for e in self.conditions])

    def set_join_function(self, v):
        self.join_operator = v

    def add_condition(self, k, op, v):
        self.conditions.append({'f': k, 'op': op, 'v': v})
