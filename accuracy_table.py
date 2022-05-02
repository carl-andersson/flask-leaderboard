from flask_table import Table, Col


class PrecCol(Col):
    def __init__(self, *args, precision=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = precision

    def td_format(self, content):
        if isinstance(content, (float,)):
            return super().td_format(f"{content:5.{self.precision}f}")
        else:
            return super().td_format(content)

class AccTable(Table):
    team = Col("Team")
    acc = PrecCol("Accuracy")
    f1 = PrecCol("F1", td_html_attrs={"style": "font-weight: bold"})
    auc = PrecCol("AUC")
    ap = PrecCol("Average precision")
    note = Col("Note")
    classes = ["styled-table"]



class AccItem:
    def __init__(self, team_id, acc, f1, auc, ap, note):
        self.team = team_id
        self.acc = acc
        self.f1 = f1
        self.auc = auc
        self.ap = ap
        self.note = note

