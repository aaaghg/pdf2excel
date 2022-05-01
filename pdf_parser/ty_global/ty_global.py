from pdf_parser.base_parser import OrderParser
from pdf_parser.ty_global.order_table import TyGlobalOrderTable
from datetime import datetime
import pdfplumber
from pdf_parser.ty_global.export_tool import TyGlobalExportTool


# data =
# {
#     order_number1: {
#         PartNo1: {
#             client, -
#             supplier, -
#             order number, -
#             product number(=PartNo),
#             product name,
#             item upc code,
#             master carton upc code,
#             order qty,
#             Packing way  (Units/carton),
#             Total Cartons/per order,
#             product specification,
#             Packing spec,
# ####        size        ####
#         },
#         PartNo2: ...,
#         ...
#     },
# ####    order_number2: ... ,
#     ...
# }
class TyGlobalParser(OrderParser):
    def __init__(self, pdf_path):
        self.client = 'Ty Global'
        self.order_table = None
        self.pdf = pdfplumber.open(pdf_path)
        self.supplier = self.get_supplier()
        self.order_number = self.get_order_number(self.pdf)

    def get_supplier(self):
        supplier = []
        p0 = self.pdf.pages[0]
        # s_rect = {"x0": 65, "top": 120, "x1": 273, "bottom": 100, "y1": 120, "y0": 100, "height": 20, "doctop": 124, "width": 209}  # supplier
        # p0.rects.append(s_rect)
        # im = p0.to_image()
        # im.draw_rects([s_rect])
        # im.save('a.jpg')
        words = p0.extract_words()
        s_bbox = (65, 120, 273, 100)
        for word in words:
            p = (int(word["x0"]), int((word["top"] + word["bottom"]) / 2))
            if self.in_bbox(p, s_bbox):
                supplier.append(word['text'])
        ret = str.join(' ', supplier)
        print(ret)
        return ret

    @staticmethod
    def get_order_number(pdf):
        words = pdf.pages[0].find_tables()[0].extract()
        # print(words)
        etd = datetime.strptime(words[1][1].strip(), "%b %d, %Y")
        result = f'{words[1][0]}\n{etd.strftime("%m/%d, %Y")}'
        return result

    def parse(self):
        only_order_number = self.order_number.split('\n')[0]
        path = f'./output/_{self.client}-PO_{only_order_number}-.xlsx'
        self.order_table = TyGlobalOrderTable(self.pdf)
        export_tool = TyGlobalExportTool(path, self.supplier, self.order_number, self.order_table)
        return export_tool
