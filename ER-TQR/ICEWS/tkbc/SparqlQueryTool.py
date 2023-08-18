import math

from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlQueryTool:
    def __init__(self):
        self.sparql_query = ""
        self.sparql_database = "http://dbpedia.org/sparql"
        self.sparql_port = SPARQLWrapper(self.sparql_database)
        self.max_num_per_time = 10000

    def set_sparql(self, sparql_query):
        self.sparql_query = sparql_query

    def calculate_search_time(self, total_num):
        if total_num < self.max_num_per_time:
            return 1
        else:
            search_times = math.ceil(total_num / self.max_num_per_time)
            return search_times

    """
    No Use
    """

    def get_num_by_sparql(self, one_sparql):
        self.sparql_port.setTimeout(3)
        try:
            self.sparql_port.setQuery(one_sparql)
            self.sparql_port.setReturnFormat(JSON)
            results = self.sparql_port.query().convert()
            res_num = int(results['results']['bindings'][0]['callret-0']['value'])
            return res_num
        except Exception as my_exception:
            print("Can't get num {}.".format(my_exception))
            return -1

    def get_sparql_query_answer(self):
        query_result_list = []

        cnt = 0
        while True:
            tmp_query = self.sparql_query + " limit 10000  offset " + str(10000 * cnt)
            print(tmp_query)
            cnt += 1
            self.sparql_port.setQuery(tmp_query)
            self.sparql_port.setReturnFormat(JSON)
            results = self.sparql_port.query().convert()
            print(results)
            var_list = results['head']['vars']
            res_list = results['results']['bindings']
            if len(res_list) == 0:
                break
            for one_res in res_list:
                one_dict = {}
                for var in var_list:
                    one_dict[var] = one_res[var]['value']
                query_result_list.append(one_dict)

        return var_list, query_result_list


if __name__ == "__main__":
    sparql = '''SELECT ?book ?com
                WHERE {
                    ?book rdf:type dbo:Book.
                    ?book rdfs:comment ?com.
                }'''
    sqt = SparqlQueryTool()
    sqt.set_sparql(sparql)
    sqt.get_sparql_query_answer()
