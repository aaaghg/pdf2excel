from pdf_parser.ty_global.order_grouping import OrderGroup


class OrderTable:
    def __init__(self, text):
        self.original_text = text


# data =
# {
#     PartNo1: {
#         product number(=PartNo),
#         product name,
#         item upc code,
#         master carton upc code,
#         order qty,
#         Packing way  (Units/carton),
#         Total Cartons/per order,
#         product specification,
#         Packing spec,
# ####    size    ####
#     },
#     PartNo2: ...,
#         ...
#     },
#     ...
# }
class TyGlobalOrderTable(OrderTable):
    def __init__(self, pdf):
        self.header = None
        self.header0 = None
        self.header1 = None
        self.empty_line = ['', '', '', '', None, '', '']
        text = self.extract_text_from_order_table(pdf)
        super(TyGlobalOrderTable, self).__init__(text)
        # self.print_order_table(text)
        self.data = self.parse()

    @staticmethod
    def print_order_table(order_table_text):
        for text in order_table_text:
            foo = ['None' if v is None else v for v in text]
            print('\t'.join(foo))

    def extract_text_from_order_table(self, pdf):
        order_table_text = []
        for page in pdf.pages:
            table_settings = {"vertical_strategy": "lines",
                              "horizontal_strategy": "text",
                              "snap_tolerance": 1, }
            texts = page.extract_table(table_settings)
            if self.header0 is None:
                self.header0 = texts[0]
                order_table_text.append(self.header0)
            if self.header1 is None:
                self.header1 = texts[1]
                order_table_text.append(self.header1)

            for text in texts:
                if text == self.header0 or text == self.header1:
                    continue
                if text == self.empty_line:
                    continue
                if text[1] is None and text[2] is None and text[3] is None:
                    continue
                order_table_text.append(text)
        foo = ['' if v is None else v for v in self.header0]
        bar = ['' if v is None else v for v in self.header1]
        self.header = [s1 + " " + s2 for s1, s2 in zip(foo, bar)]
        print(self.header)
        return order_table_text

    # @staticmethod
    # def handle_group(group):
    #     return group

    def parse(self):
        return OrderGroup.group_orders(self.original_text)


