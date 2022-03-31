# import setup
import config as cf
import export_charts
import export_to_sheets as ets
from extract_from_polarion import polarian_data

print("---Connecting to Polarion---")


def main():
    """
    Function to connect to polarion portal and extract the required data using queries amd return the result for populating in the email report.
    """
    config = cf.Config()
    config.load()
    pol_obj = polarian_data()

    print("\n-----Extracting from Polarion-----")
    res = []
    data = pol_obj.extract_data(config)
    print("\n Printing type ", type(data))
    print("\nData :", data)
    res.append(data)

    print("\n---Exporting in sheets")
    sheets_obj = ets.export_data()
    row_count = sheets_obj.export_sheets(data, config)
    chart_obj = export_charts.Charts(config.file_name, config.GS_CREDENTIALS)
    if row_count == "3":
        chart_obj.create_charts(config.tags, row_count)
    else:
        chart_obj.update_charts(config.tags, row_count)

    print("\n-----Extracting component wise data from Polarion-----")
    component_data = pol_obj.extract_component_data(config)
    print("\n Printing type of component data", type(component_data))
    print("\nComponent data :", component_data)
    res.append(component_data)

    print("\n-----Extracting component wise total testcase from Polarion-----")
    component_total_tc = pol_obj.extract_component_total_tc(config)
    print("\nPrinting type of component total testcases", type(component_total_tc))
    print("\nComponent wise total testcases :", component_total_tc)
    res.append(component_total_tc)

    print("\nResults: ", res)
    return res


if __name__ == "__main__":
    main()
