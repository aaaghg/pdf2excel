from enum import IntEnum
import copy


class GroupType(IntEnum):
    NotDefine = -1
    ProductOrder = 0,
    CasePack = 1,
    ProductSpec = 2,
    PackingSpec = 3,
    ZZ = 99,


class OrderGroup:
    def __init__(self, group):
        self.group = group[:]
        self.group_type = GroupType.NotDefine
        self.name = self.get_name()

    def __repr__(self):
        return str(self.group)

    @staticmethod
    def factory(group):
        grp_type = OrderGroup.get_group_type(group)
        if grp_type == GroupType.ProductOrder:
            return ProductOrderGroup(group)
        elif grp_type == GroupType.CasePack:
            return CasePackGroup(group)
        elif grp_type == GroupType.ProductSpec:
            return PackingSpecGroup(group)
        elif grp_type == GroupType.PackingSpec:
            return PackingSpecGroup(group)
        elif grp_type == GroupType.ZZ:
            return ZZGroup(group)

    @staticmethod
    def get_group_type(group):
        ret = GroupType.NotDefine
        try:
            if group[0][1].isdigit():
                return GroupType.ProductOrder
            elif 'CASE PACK:' in group[0][3]:
                return GroupType.CasePack
            elif 'PRODUCT SPECIFICATIONS:' in group[0][3]:
                return GroupType.ProductSpec
            elif 'PACKAGING SPECIFICATIONS:' in group[0][3]:
                return GroupType.PackingSpec
            elif 'ZZ‐' in group[0][1]:
                return GroupType.ZZ
            else:
                return ret
        except:
            return ret

    # groups
    # |_packing_group1
    #   |_order_group1
    #   |_order_group2
    #   |_...
    # |_packing_group2
    #   |_...
    # |_...
    @staticmethod
    def group_orders(order_texts):
        groups = dict()
        packing_group = dict()
        current_group = []
        for index in range(2, len(order_texts)):
            text = order_texts[index]
            # It means the end of previous group and a start of new group when got a row with some condition as following
            # 'ORD QTY' and 'OUR PART NO.' has value,
            # CASE PACK:
            # PRODUCT SPECIFICATIONS:
            # PACKAGING SPECIFICATIONS:
            # If got above keywords, it need to end up the existing collection
            if (text[0] != '' and text[1].isdigit()) or 'CASE PACK:' in text[3] or 'PRODUCT SPECIFICATIONS:' in text[3] or 'PACKAGING SPECIFICATIONS:' in text[3]:
                # move the collection of current_group to packing_group
                if len(current_group) > 0:  # previous group had been collected
                    order_group = OrderGroup.factory(current_group)
                    packing_group[order_group.name] = order_group
                    current_group.clear()
                # if the packing_group has collect all needed value, move it to groups
                if 'CASE PACK:' in packing_group and 'PRODUCT SPECIFICATIONS:' in packing_group and 'PACKAGING SPECIFICATIONS:' in packing_group:
                    new_index = len(groups)
                    groups[new_index] = copy.deepcopy(packing_group)
                    packing_group = dict()  # restart a new packing_group
                current_group.append(text)
            else:
                current_group.append(text)

        if current_group is not None:
            order_group = OrderGroup.factory(current_group)
            packing_group[order_group.name] = order_group
            current_group.clear()
        if packing_group is not None:
            new_index = len(groups)
            groups[new_index] = copy.deepcopy(packing_group)
        return groups

    def get_name(self):
        pass

    def get_text(self):
        ret = []
        for row in self.group:
            ret.append(row[3])
        return '\n'.join(ret)


class ProductOrderGroup(OrderGroup):
    def __init__(self, group):
        super(ProductOrderGroup, self).__init__(group)
        # handle the line feed in the product name
        item_upc_line_no = self.get_item_upc_line_no()
        self.product_name = self.get_product_name()
        self.group[0][3] = self.product_name
        for i in range(1, item_upc_line_no):
            del self.group[i]
        self.group_type = self.get_group_type(group)

    def get_product_name(self):
        item_upc_line_no = self.get_item_upc_line_no()
        product_name = ' '.join([self.group[i][3] for i in range(0, item_upc_line_no)])
        return product_name

    def get_item_upc_line_no(self):
        for row in self.group:
            if 'ITEM UPC:' in row[3]:
                return self.group.index(row)
        return -1

    def get_carton_upc_line_no(self):
        for row in self.group:
            if 'CARTON UPC' in row[3]:
                return self.group.index(row)
        return -1

    def get_name(self):
        name = self.group[0][1]
        return name


class CasePackGroup(OrderGroup):
    def __init__(self, group):
        super(CasePackGroup, self).__init__(group)
        self.group_type = self.get_group_type(group)

    def get_name(self):
        return self.group[0][3]


class ProductSpecGroup(OrderGroup):
    def __init__(self, group):
        super(ProductSpecGroup, self).__init__(group)
        self.group_type = self.get_group_type(group)

    def get_name(self):
        return self.group[0][3]


class PackingSpecGroup(OrderGroup):
    def __init__(self, group):
        super(PackingSpecGroup, self).__init__(group)
        self.group_type = self.get_group_type(group)

    def get_name(self):
        return self.group[0][3]


class ZZGroup(OrderGroup):
    def __init__(self, group):
        super(ZZGroup, self).__init__(group)
        self.group_type = self.get_group_type(group)

    def get_name(self):
        return self.group[0][1]

