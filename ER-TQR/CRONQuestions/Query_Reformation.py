from Empty_Answer_Query import eaqs
from RuleBased.SparqlParser import SparqlParser
import os

from SimiBased.SparqlQueryTool import SparqlQueryTool

min_simi_threshold = 0.8
root_folder = "./result/"
dbr = "http://dbo_plain.org/resource/"
dbo = "http://dbo_plain.org/ontology/"
relaxed_answer_folder = "./relaxed_answer/"


class QueryReform:
    def __init__(self, sparql, query_number):
        self.sparql = sparql
        self.query_number = str(query_number)
        a = SparqlParser(sparql=sparql)
        a.parse_sparql()
        self.er_name_list = a.e_name_list[:]
        self.er_name_list.extend(a.r_name_list)

        self.alter_dict = {}
        self.res_sparql_alter_list = []
        self.res_sparql_list = []

    def get_name_alternative(self):
        for er_name in self.er_name_list:
            alter_e_file = root_folder + er_name.split(":")[-1] + ".txt"
            if er_name not in self.alter_dict:
                self.alter_dict[er_name] = [[er_name, 0]]
            with open(alter_e_file, 'r', encoding="UTF-8") as f:
                for line in f.readlines():
                    n, s = line.split()
                    if float(s) >= min_simi_threshold:
                        continue
                    self.alter_dict[er_name].append([n, float(s)])

    def get_reformed_sparql(self):
        self.get_name_alternative()
        self.get_combination(0, [])
        self.res_sparql_alter_list.sort(key=lambda x: x[1])
        for res_sparql_alter in self.res_sparql_alter_list:
            tmp_sparql = self.sparql[:]
            cost = res_sparql_alter[1]
            for idx in range(len(res_sparql_alter)):
                altered_name = res_sparql_alter[0][idx]
                if ":" in altered_name or "=" in altered_name or "(" in altered_name or "'" in altered_name or ")" in altered_name or "," in altered_name:
                    altered_name = altered_name.replace("dbo:", dbo)
                    altered_name = altered_name.replace("dbr:", dbr)
                    if not altered_name.startswith("<"):
                        altered_name = "<" + altered_name
                    if not altered_name.endswith(">"):
                        altered_name = altered_name + ">"
                tmp_sparql = tmp_sparql.replace(self.er_name_list[idx], altered_name)
                tmp_sparql = " ".join(tmp_sparql.split())
            self.res_sparql_list.append([tmp_sparql, cost])

    def get_relaxed_answer(self):
        sqt = SparqlQueryTool()
        if not os.path.exists(relaxed_answer_folder):
            os.mkdir(relaxed_answer_folder)

        with open(relaxed_answer_folder + "E"+self.query_number + ".txt", 'w', encoding="UTF-8") as f:
            for res_sparql in self.res_sparql_list:
                sqt.set_sparql(res_sparql[0])
                var_list, query_result_list = sqt.get_sparql_query_answer()
                # if len(query_result_list) == 0:
                #     continue
                f.write("{}\t{}\n".format(res_sparql[1], res_sparql[0]))
                for one_query_res in query_result_list:
                    for var in var_list:
                        f.write("?{}\t{}\t".format(var, one_query_res[var]))
                    f.write("\n")
                f.write("\n")

    def get_combination(self, altered_name_idx, path):
        if altered_name_idx >= len(self.er_name_list):
            return
        name = self.er_name_list[altered_name_idx]

        for candidate in self.alter_dict[name]:
            tmp = path[:]
            tmp.append(candidate)
            if altered_name_idx == len(self.er_name_list) - 1:
                total_cost = 0
                one_alter = []
                for name, one_cost in tmp:
                    one_alter.append(name)
                    total_cost += one_cost
                if total_cost <= min_simi_threshold:
                    self.res_sparql_alter_list.append([one_alter, total_cost])
            else:
                self.get_combination(altered_name_idx + 1, tmp)


if __name__ == "__main__":
    idx_list = [0]
    for idx, sparql_query in enumerate(eaqs):
        if idx not in idx_list:
            continue
        qr = QueryReform(sparql_query, idx + 1)
        qr.get_reformed_sparql()
        qr.get_relaxed_answer()
