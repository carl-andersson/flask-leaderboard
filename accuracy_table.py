
def format_elem(content):
    if isinstance(content, (float,)):
        return format(content, "1.3f")
    else:
        return content

class AccItem:
    def __init__(self, team_id, acc, f1, auc, ap, note):
        self.team = team_id
        self.acc = format_elem(acc)
        self.f1 = format_elem(f1)
        self.auc = format_elem(auc)
        self.ap = format_elem(ap)
        self.note = note

