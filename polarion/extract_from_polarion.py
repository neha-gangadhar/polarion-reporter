class polarian_data:
    """
    Module to extract data from polarion portal based on different queries.
    """

    # Below import is done inside class to reduce connection time to polarion.
    from pylero.work_item import TestCase

    def extract_data(self, config):
        """
        Function to fetch tier wise data from polarion.
        """
        data = {}
        for i in config.tags:
            data[str(i)] = []
            for filter_keys in config.filter.keys():
                for val in config.filter[filter_keys]["values"]:
                    query = (
                        config.filter[filter_keys]["keys"]
                        + ":"
                        + val
                        + " AND "
                        + config.key
                        + ":"
                        + str(i)
                        + " AND project.id:"
                        + config.project_id
                        + " AND "
                        "NOT status" + ":" + "inactive"
                    )

                    print(query)
                    tc = self.TestCase.get_query_result_count(query)
                    data[str(i)].append(tc)

        return data

    def extract_component_total_tc(self, config):
        """
        Function to fetch total testcase count per component from polarion
        """
        component_total_tc = {}
        for component_filter_keys in config.component_filter.keys():
            for val in config.component_filter[component_filter_keys]["values"]:
                component_total_tc[str(val)] = []
                for i in config.tags:
                    query = (
                        config.component_filter[component_filter_keys]["keys"]
                        + ":"
                        + val
                        + " AND "
                        + config.key
                        + ":"
                        + str(i)
                        + " AND project.id:"
                        + config.project_id
                        + " AND "
                        "status" + ":" + "approved"
                    )
                    print(query)
                    tc = self.TestCase.get_query_result_count(query)
                    component_total_tc[str(val)].append(tc)

        return component_total_tc

    def extract_component_data(self, config):
        """
        Function to fetch tier wise automated tc count for each component from polarion.
        """
        component_data = {}
        for component_filter_keys in config.component_filter.keys():
            for val in config.component_filter[component_filter_keys]["values"]:
                component_data[str(val)] = []
                for i in config.tags:
                    query = (
                        config.component_filter[component_filter_keys]["keys"]
                        + ":"
                        + val
                        + " AND "
                        + config.key
                        + ":"
                        + str(i)
                        + " AND project.id:"
                        + config.project_id
                        + " AND caseautomation.KEY:automated"
                        + " AND "
                        "status" + ":" + "approved"
                    )
                    print(query)
                    tc = self.TestCase.get_query_result_count(query)
                    component_data[str(val)].append(tc)

        return component_data
