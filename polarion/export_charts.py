import json

import pygsheets
import yaml

import gapi_json


class Charts:
    """
    Class for all charts related tasks like format, creation, updation.
    """

    def __init__(self, filename, gs_cred):
        self.gc = pygsheets.authorize(service_account_file=gs_cred)
        # self.gc = pygsheets.authorize(client_secret = gs_cred)
        self.sh = self.gc.open(filename)

        self.wc = self.sh.worksheet(0)

    def formatting(self):
        """
        Function for formatting data.
        """
        data = {
            "spec": {
                "basicChart": {"chartType": "LINE", "headerCount": 1, "domains": [{""}]}
            },
            "position": {
                "overlayPosition": {"anchorCell": {"rowIndex": 10, "columnIndex": 1}}
            },
        }
        return data

    def yaml_convert_to_list(self):
        """
        Function to load content from yaml and convert to list
        """
        with open(r"config/config.yaml") as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
        print(dict)
        tags = dict.get("tags")
        return tags

    def create_charts(self, tags, row_count):
        """
        Function to create charts.
        """
        ch1 = "B"
        ch2 = "C"
        ch3 = "D"
        ch4 = "A"
        row_c = str(int(row_count) + 1)
        k = 0
        for i in tags:
            if k % 2 == 0:
                ch4 = "A"
                row_c = int(row_c)
                if k == 0:
                    row_c = row_c + 0
                else:
                    row_c = row_c + 20
                row_c = str(row_c)
                k = k + 1
            elif k % 2 == 1:
                ch4 = "H"
                k = k + 1
            pygsheets.Chart(
                self.wc,
                title=i.capitalize(),
                chart_type=pygsheets.custom_types.ChartType.LINE,
                domain=("A2", "A" + row_count),
                ranges=[
                    (ch1 + "2", ch1 + row_count),
                    (ch2 + "2", ch2 + row_count),
                    (ch3 + "2", ch3 + row_count),
                ],
                anchor_cell=ch4 + row_c,
            )

            ch1 = chr(ord(ch1) + 3)
            ch2 = chr(ord(ch2) + 3)
            ch3 = chr(ord(ch3) + 3)

    def update_charts(self, tags, row_count):
        """
        Function to update charts.
        """
        ch1 = "B"
        ch2 = "C"
        ch3 = "D"
        ch4 = "A"
        k = 0
        row_c = str(int(row_count) + 1)
        for i in tags:
            chart_list = self.wc.get_charts(title=i.capitalize())
            l = len(chart_list)
            for j in range(0, l):
                if k % 2 == 0:
                    ch4 = "A"
                    row_c = int(row_c)
                    if k == 0:
                        row_c = row_c + 0
                    else:
                        row_c = row_c + 20
                    row_c = str(row_c)
                    k = k + 1
                elif k % 2 == 1:
                    ch4 = "H"
                    k = k + 1
                chart_list[j].ranges = [
                    (ch1 + "2", ch1 + row_count),
                    (ch2 + "2", ch2 + row_count),
                    (ch3 + "2", ch3 + row_count),
                ]
                chart_list[j].domain = ("A2", "A" + row_count)
                chart_list[j].anchor_cell = ch4 + row_c
                chart_list[j].update_chart()
                ch1 = chr(ord(ch1) + 3)
                ch2 = chr(ord(ch2) + 3)
                ch3 = chr(ord(ch3) + 3)
