import enum

import Entry


class CategoryId(enum.Enum):
    id_1 = 1,
    id_2 = 2,
    id_3 = 3,
    id_4 = 4,
    id_5 = 5,
    id_6 = 6,
    id_7 = 7,
    id_8 = 8,
    id_9 = 9,
    id_10 = 10,
    id_11 = 11,
    id_12 = 12,
    id_13 = 13,
    id_14 = 14,


def build_category_description():
    categories = {}
    filename = 'analytics\\category.str'
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.split(':')
            category_number = int(s[0].strip())
            category_desc = str(s[1].strip())
            for v, m in CategoryId.__members__.items():
                if m.value[0] == category_number:
                    categories[v] = category_desc
    return categories

_categories = build_category_description()


class CartTransactionCategory(object):
    def match(self, entry):
        pass


def build_transfer_category_critiria():
    d = {}
    filename = 'analytics\\TransferCategory.criteria'
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.split(':')
            acc_number = str(s[0].strip())
            category_id = int(s[1].strip())
            for v, m in CategoryId.__members__.items():
                if m.value[0] == category_id:
                    d[acc_number] = m
    return d


_transfer_category_critiria = build_transfer_category_critiria()


class TransferCategory(object):
    def match(self, entry):
        acc_number = entry.acc_number()
        try:
            return _transfer_category_critiria[acc_number]
        except KeyError:
            return None


class Category(object):
    """description of class"""
    def guess(self, entry):
        type_id = Entry.OperationMap[entry.type()]
        if type_id == Entry.OperationType.CART_TRANSACTION:
            return CartTransactionCategory().match(entry)
        elif type_id == Entry.OperationType.TRANSFER_OUT or type_id == Entry.OperationType.TRANSFER_IN:
            return TransferCategory().match(entry)
    def description(self, category_id):
        return _categories[category_id.name]
