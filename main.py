import pdfplumber
from pdf_parser.ty_global.ty_global import TyGlobalParser
import os

# def in_rect(point, rect):
#     px, py = point
#     p1, p2, p3, p4 = rect
#     if p1[0] <= px <= p2[0] and p1[1] < py <= p3[1]:
#         return True
#     else:
#         return False


def in_bbox(point, bbox):
    px, py = point
    p1, p2, p3, p4 = bbox
    if p1 <= px <= p3 and p4 < py <= p2:
        return True
    else:
        return False


def get_supplier():
    file = r"D:\code\work\pypdfexcel\input\309210 House Dollar misting diffusers 20220317.pdf"
    supplier = []
    with pdfplumber.open(file) as pdf:
        p0 = pdf.pages[0]
        srect = {"x0": 65, "top": 120, "x1": 273, "bottom": 100}  # supplier
        p0.rects.append(srect)
        im = p0.to_image()
        im.draw_rects([srect])
        im.save('a.jpg')
        words = p0.extract_words()
        sbbox = (65, 120, 273, 100)
        for word in words:
            p = (int(word["x0"]), int((word["top"]+word["bottom"])/2))
            if in_bbox(p, sbbox):
                supplier.append(word['text'])
        ret = str.join(' ', supplier)
        print(ret)
        return ret


def get_order_table():
    file = r"D:\code\work\pypdfexcel\input\309210 House Dollar misting diffusers 20220317.pdf"
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            print(tables)
            for table in tables:
                print(table.extract())


def show_all_table():
    file = r"D:\code\work\pypdfexcel\input\309210 House Dollar misting diffusers 20220317.pdf"
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            print(tables)
            for table in tables:
                print(table.extract())


def test():
    file = r"D:\code\work\pypdfexcel\input\309210 House Dollar misting diffusers 20220317.pdf"
    with pdfplumber.open(file) as pdf:
        p0 = pdf.pages[0]
        table = p0.extract_table()
        tables = p0.extract_tables()
        words = p0.extract_words()
        print('words')
        print(words)
        # print(p0.chars)
        bbox = (420, 42, 588, 58)
        bpage = p0.crop(bbox)
        sbox = (66, 100, 203, 120)  # supplier
        spage = p0.crop(sbox)
        print(spage.rects)
        bim = p0.to_image()
        bim.draw_rects(bpage.rects)
        bim.draw_rects(spage.rects)
        bim.save('b.jpg')
        print('bpage')
        print(bpage.extract_text())
        print('lines')
        print(p0.lines)
        print('rects')
        print(p0.rects)
        print(table)
        print(tables)
        print('dedupe_chars')
        print(p0.dedupe_chars())
        findtables = p0.find_tables()
        for t in findtables:
            print('extract table==================')
            print(t.extract())
        # print(p0.extract_words())
        # print(p0.extract_text())
        im = p0.to_image()
        im.draw_rects(p0.extract_words())
        im.save('a.jpg')


def do_something():
    # file = r"D:\code\work\pypdfexcel\input\309210 House Dollar misting diffusers 20220317.pdf"
    file = r"D:\code\work\pypdfexcel\input\309203 Comfort Slippers Q4 20220224 rev 3 20220307.pdf"
    parser = TyGlobalParser(file)
    export_tool = parser.parse()
    export_tool.export()


def parse_all_pdf():
    files = list()
    input_dir = './input/'
    for input_dir_path, _, filenames in os.walk(input_dir):
        for f in filenames:
            files.append(os.path.abspath(os.path.join(input_dir_path, f)))
    print(files)
    for file in files:
        parser = TyGlobalParser(file)
        export_tool = parser.parse()
        export_tool.export()


if __name__ == '__main__':
    # test()
    # show_all_table()
    parse_all_pdf()
