from modules.runners.run import RunResult

DEC_COLS = [10, 100, 1000, 10000, 100000]


def rround(num: float, decs=2):
    i = 0
    while num > DEC_COLS[decs-1]:
        i += 1
        num /= 10
    num = round(num)
    while i > 0:
        i -= 1
        num *= 10
    return num


class Selector:
    def get_value(self, row: RunResult):
        return ""


class NullSelector(Selector):
    def get_value(self, row: RunResult):
        return 0


class KeySelector(Selector):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def get_value(self, row: RunResult):
        return row.keys.get(self.key, "-")


class ParamSelector(Selector):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def get_value(self, row: RunResult):
        return row.param_list[self.num]


class ResultSelector(Selector):
    def __init__(self, col):
        super().__init__()
        self.col = col

    def get_value(self, row: RunResult):
        return row.result_list[self.col]


class Col:
    def __init__(self, name, selector: Selector = Selector(), unit="-", line_after=False):
        self.name = name
        self.selector = selector
        self.line_after = line_after
        self.unit = unit

    def get_data(self, data_row):
        res = self.selector.get_value(data_row)
        if res == '"-"' or res is None:
            return "-"
        if isinstance(res, str):
            return res
        return "{:.0f}".format(rround(float(res)))

    def get_unit(self):
        return self.unit


class NumCol(Col):
    def get_data(self, data_row):
        res = self.selector.get_value(data_row)
        return "{:.0f}".format(rround(float(res)))


class PercentageCol(Col):
    def get_data(self, data_row):
        res = self.selector.get_value(data_row)
        if res == '"-"' or res is None:
            return "-"
        return "{:.0f}".format(rround(float(min(100, 100 * float(res)))))

    def __init__(self, name, selector: Selector = Selector(), unit="\\%"):
        super(PercentageCol, self).__init__(name, selector, unit=unit)


def euro_render(res):
    strr = "{:.0f}".format(float(res))
    if len(strr) < 6:
        return strr
    ll = 0
    res_str = ""
    while ll < len(strr):
        res_str += strr[ll]
        if (ll - len(strr)) % 3 == 2:
            res_str += " "
        ll += 1
    return res_str


class EurCol(Col):
    def get_data(self, data_row):
        res = self.selector.get_value(data_row)
        if res == '"-"' or res is None:
            return "-"
        return euro_render(rround(float(res), decs=3))

    def __init__(self, name, selector: Selector = Selector(), unit="\\euro"):
        super(EurCol, self).__init__(name, selector, unit=unit)


class EurColPops(Col):
    def get_data(self, data_row):
        if self.rr:
            res = rround(float(self.selector.get_value(data_row)) * float(data_row.keys["POPS"]), decs=3)
        else:
            try:
                res = float(self.selector.get_value(data_row)) * float(data_row.keys["POPS"])
                return res/1000000
            except ValueError:
                return 0
        if res == '"-"' or res is None:
            return "-"
        return euro_render(res)

    def __init__(self, name, selector: Selector = Selector(), unit="\\euro", rr=True):
        super(EurColPops, self).__init__(name, selector, unit=unit)
        self.rr = rr
        print(self.rr)


class SensSpecCalc(Col):
    def __init__(self, name, top_row: Selector, bot_row: Selector, neg=False, unit="\\%"):
        super(SensSpecCalc, self).__init__(name, bot_row, unit=unit)
        self.top_row = top_row
        self.bot_row = bot_row
        self.neg = neg

    def get_data(self, data_row):
        t = self.top_row.get_value(data_row)
        u = self.bot_row.get_value(data_row)
        if self.neg:
            u = 1 - float(u)
        return "{:.0f}".format(rround(float(min(100.0, 100 * float(t) / float(u)))))


class ConditionalCalc(Col):
    def __init__(self, name, top_row: Selector, bot_row: Selector, botrow2: Selector = NullSelector(), neg=False,
                 unit="-", line_after=False):
        super(ConditionalCalc, self).__init__(name, bot_row, unit, line_after=line_after)
        self.top_row = top_row
        self.bot_row = bot_row
        self.bot_row2 = botrow2
        self.neg = neg

    def get_data(self, data_row):
        t = self.top_row.get_value(data_row)
        u = self.bot_row.get_value(data_row)
        if self.neg:
            u = 1 - float(u)
        return "{:.0f}".format(rround(float(t) / float(u)))


class EuroConditionalCalc(Col):
    def __init__(self, name, top_row: Selector, bot_row: Selector, botrow2: Selector = NullSelector(), neg=False,
                 unit="\\euro", rr=True):
        super(EuroConditionalCalc, self).__init__(name, bot_row, unit=unit)
        self.rr = rr
        self.top_row = top_row
        self.bot_row = bot_row
        self.bot_row2 = botrow2
        self.neg = neg

    def get_data(self, data_row):
        t = self.top_row.get_value(data_row)
        u = self.bot_row.get_value(data_row)
        if self.neg:
            u = 1 - u
        if self.rr:
            return "{:.0f}".format(rround(float(t) / float(u)))
        else:
            return "{:.0f}".format((float(t) / float(u)))


class MultCol(Col):
    def __init__(self, name, top_row: Selector, bot_row: Selector, neg=False, unit="\\%", rr=True):
        super(MultCol, self).__init__(name, bot_row, unit=unit)
        self.top_row = top_row
        self.bot_row = bot_row
        self.neg = neg
        self.rr = rr

    def get_data(self, data_row):
        t = self.top_row.get_value(data_row)
        u = self.bot_row.get_value(data_row)
        if self.neg:
            u = 1 - float(u)
        if self.rr:
            return "{:.0f}".format(rround(float(t) * float(u)))
        else:
            return "{:.0f}".format(float(t) * float(u))
