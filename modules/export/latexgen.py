from modules.export.data import Col


class Generator:
    def __init__(self, col_list: list[Col]):
        self.col_list = col_list

    def gen(self, dataa):
        for data_id in dataa:
            data = dataa[data_id]
            a = " "
            first = True
            for c in self.col_list:
                if first:
                    a += "c "
                else:
                    a += "| c"
                first = False
            dat = ""
            started = False
            for col in self.col_list:
                if started:
                    dat += " & "
                dat += col.name
                started = True
            dat += "\\\\\\hline\n"
            dat = ""
            rw = False
            for row in data:
                if rw:
                    dat = dat + "\n"
                rw = True
                started = False
                for col in self.col_list:
                    if started:
                        dat += " & "

                    dat += col.get_data(row)
                    started = True
                dat += "\\\\"
            return dat


class RowGenerator:
    def __init__(self, col_list: list[Col]):
        self.col_list = col_list

    def gen(self, data):
        dat = ""
        for col in self.col_list:
            col_r = ''
            for row in data:
                if col_r != "":
                    col_r+=" & "
                col_r += col.get_data(row)
            dat += "{} & {} & {} \\\\ ".format(col.name, col_r, col.get_unit())
            if col.line_after:
                dat += "\\hline"
            dat += "\n"
        return dat
