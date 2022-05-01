class OrderParser:
    # bbox: [x0, top, x1, bottom]
    @staticmethod
    def in_bbox(point, bbox):
        px, py = point
        p1, p2, p3, p4 = bbox
        if p1 <= px <= p3 and p4 < py <= p2:
            return True
        else:
            return False
