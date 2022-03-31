import datetime
from tracemalloc import start

from gspread_formatting import set_column_width


class export_data:
    """
    Class to export data to googlesheets.
    """

    import gspread
    from gspread.exceptions import SpreadsheetNotFound

    def next_available_row(self, worksheet):
        """
        Function calculates next available row in the gsheet
        """
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)

    def format_cell(self):
        """
        Function to format the cells
        """
        return {
            "horizontalAlignment": "CENTER",
            "borders": {
                "top": {"style": "SOLID", "width": 1},
                "bottom": {"style": "SOLID", "width": 1},
                "left": {"style": "SOLID", "width": 1},
                "right": {"style": "SOLID", "width": 1},
            },
        }

    def export_sheets(self, data, config):
        """
        Function to export the data fetched from polarion to gsheet.
        """
        gc = self.gspread.service_account(filename=config.GS_CREDENTIALS)
        try:
            sh = gc.open(config.file_name)
        except self.SpreadsheetNotFound:
            print(
                "Spreadsheets in not exits or you have not shared with client email id"
            )
        ws = sh.get_worksheet(0)
        if self.next_available_row(ws) == "1":
            ws.update("A1", "Tier Classification")
            set_column_width(ws, "A", 150)

            start_c = "B"
            for keys in data.keys():
                end_c = chr(ord(start_c) + 2)
                cell_merge_name = start_c + str(1) + ":" + end_c + str(1)
                ws.merge_cells(cell_merge_name)
                print(start_c + str(1))
                ws.update(start_c + str(1), keys.capitalize())
                t_s = start_c
                for filter_keys in config.filter.keys():
                    for val, label in zip(
                        config.filter[filter_keys]["values"],
                        config.filter[filter_keys]["labels"],
                    ):
                        query = (
                            config.url
                            + r"/#/workitems?query="
                            + config.key
                            + "%3A"
                            + keys
                            + r"%20AND%20"
                            + config.filter[filter_keys]["keys"]
                            + r"%3A"
                            + val
                            + r"%20AND%20project.id%3A"
                            + config.project_id
                        )

                        val_insert = r'=HYPERLINK("' + query + r'","' + label + r'")'
                        ws.update_acell(t_s + str(2), val_insert)

                        t_s = chr(ord(t_s) + 1)
                start_c = chr(ord(start_c) + 3)
            strr = chr(ord("A") + (len(data.keys()) * 3))
            ws.format("A1:" + strr + str(2), self.format_cell())
            ws.update("A2", "Day")

        row_count = self.next_available_row(ws)

        print(row_count)
        day = str(datetime.datetime.now()).split(".")[0]
        print(day)
        ws.update("A" + row_count, day)
        start_c = "B"
        for keys in data.keys():
            t_s = start_c
            for val in data[keys]:
                ws.update(t_s + row_count, val)
                t_s = chr(ord(t_s) + 1)
            start_c = chr(ord(start_c) + 3)
        strr = chr(ord("A") + (len(data.keys()) * 3))
        ws.format("A" + row_count + ":" + strr + row_count, self.format_cell())

        return row_count
