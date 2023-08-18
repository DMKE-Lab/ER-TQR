from scipy.stats import entropy
import numpy as np
import scipy
import os

from SimiBased.SimiBasedParams import alpha, js_top_k, miu_o, \
    miu_s


class SimiGraph:
    def __init__(self, triple2idx_file, e2idx_file, r2idx_file):
        self.triple2idx_file = triple2idx_file
        self.e2idx_file = e2idx_file
        self.r2idx_file = r2idx_file

        self.e_name2idx = {}
        self.e_idx2name = {}
        self.r_name2idx = {}
        self.r_idx2name = {}

        """
        Unigram of entity, w_id is e_id
        {
            e_id:{w_id:num, w_id:num,...},
            ...
        }
        """
        self.U_e_w_num = {}

        """
        Unigram of entity, recording total num of w_id for a e_id
        {
            e_id:num, e_id:num, ...
        }
        """
        self.U_e_num = {}

        """
        Bigram of entity, w is w_token which is composed of 'e_id,r_id'
        {
            e_id:{w_token:num, w_token:num, ...}, 
            ...
        }
        """
        self.B_e_w_num = {}

        """
        Bigram of entity, recording total num of w_token for a e_id
        {
            e_id:num, e_id:num, ...
        }
        """
        self.B_e_num = {}

        """
        Unigram of entity, occurred times for every w_id
        {
            w_id:num, w_id:num, ...
        }
        """
        self.U_w_num = {}

        """
        Bigram of entity, occured times for every w_token
        {
            w_token:num, w_token:num, ...
        }
        """
        self.e_B_w_num = {}

        """
        Subject of relation, w_id is the e_id which is the subject of r_id
        {
            r_id:{w_id:num, w_id:num, ...}, 
            ...
        }
        """
        self.S_r_w_num = {}

        """
        Subject of relation, total num of the subject of a r_id
        {
            r_id:num, r_id:num, ...
        }
        """
        self.S_r_num = {}

        """
        Object of relation, w_id is the e_id which is the object of r_id
        {
            r_id:{w_id:num, w_id:num, ...},
            ...
        }
        """
        self.O_r_w_num = {}

        """
        Object of relation, total num of object of a r_id
        {
            r_id:num, r_id:num, ...
        }
        """
        self.O_r_num = {}

        """
        Subject_Object of relation, w_token is composed of 'subject_id,object_id'
        {
            r_id:{w_token:num, w_token:num, ...},
            ...
        }
        """
        self.B_r_w_num = {}

        """
        Subject_Object of relation, total num of Subject_Object of a r_id
        {
            r_id:num, r_id:num, ...
        }
        """
        self.B_r_num = {}

        """
        Subject_Object of relation, occurred times per w_token ('subject_id,object_id')
        """
        self.r_B_w_num = {}

        """
        Subject of relation, occurred times per w_id (subject_id)
        {
            w_id:num, w_id:num, ...
        }
        """
        self.S_w_num = {}

        """
        Object of relation, occurred times per w_id (object_id)
        {
            w_id:num, w_id:num, ...
        }
        """
        self.O_w_num = {}

        self.total_e_num = 0
        self.total_s_o_num = 0
        self.total_e_r_num = 0
        self.total_s_num = 0
        self.total_o_num = 0

    # key_e is e_id, doc_e is w_id（e_id）
    def add_U_e_w(self, key_e, doc_e):
        if key_e not in self.U_e_w_num:
            self.U_e_w_num[key_e] = {}
        if doc_e not in self.U_e_w_num[key_e]:
            self.U_e_w_num[key_e][doc_e] = 0
        self.U_e_w_num[key_e][doc_e] += 1

        if key_e not in self.U_e_num:
            self.U_e_num[key_e] = 0
        self.U_e_num[key_e] += 1

    # key_e is e_id, doc_e_r is w_token
    def add_B_e_w(self, key_e, doc_e_r):
        if key_e not in self.B_e_w_num:
            self.B_e_w_num[key_e] = {}
        if doc_e_r not in self.B_e_w_num[key_e]:
            self.B_e_w_num[key_e][doc_e_r] = 0
        self.B_e_w_num[key_e][doc_e_r] += 1

        if key_e not in self.B_e_num:
            self.B_e_num[key_e] = 0
        self.B_e_num[key_e] += 1

    # key_r is r_id, w_id is subject of r_id
    def add_S_r_w(self, key_r, w_id):
        if key_r not in self.S_r_w_num:
            self.S_r_w_num[key_r] = {}
        if w_id not in self.S_r_w_num[key_r]:
            self.S_r_w_num[key_r][w_id] = 0
        self.S_r_w_num[key_r][w_id] += 1

        if key_r not in self.S_r_num:
            self.S_r_num[key_r] = 0
        self.S_r_num[key_r] += 1

    # key_r is r_id, w_id is object of r_id
    def add_O_r_w(self, key_r, w_id):
        if key_r not in self.O_r_w_num:
            self.O_r_w_num[key_r] = {}
        if w_id not in self.O_r_w_num[key_r]:
            self.O_r_w_num[key_r][w_id] = 0
        self.O_r_w_num[key_r][w_id] += 1

        if key_r not in self.O_r_num:
            self.O_r_num[key_r] = 0
        self.O_r_num[key_r] += 1

    # key_r is r_id, w_token is 'subject_id,object_id' of r_id
    def add_B_r_w(self, key_r, w_token):
        if key_r not in self.B_r_w_num:
            self.B_r_w_num[key_r] = {}
        if w_token not in self.B_r_w_num[key_r]:
            self.B_r_w_num[key_r][w_token] = 0
        self.B_r_w_num[key_r][w_token] += 1

        if key_r not in self.B_r_num:
            self.B_r_num[key_r] = 0
        self.B_r_num[key_r] += 1

    # w_id is the id of e as subject or object
    def count_U_w_num(self, w_id):
        if w_id not in self.U_w_num:
            self.U_w_num[w_id] = 0
        self.U_w_num[w_id] += 1

    # w_token is e,r
    def count_w_of_e_B(self, w_token):
        if w_token not in self.e_B_w_num:
            self.e_B_w_num[w_token] = 0
        self.e_B_w_num[w_token] += 1

    # w_id is the subject id
    def count_S_w_num(self, w_id):
        if w_id not in self.S_w_num:
            self.S_w_num[w_id] = 0
        self.S_w_num[w_id] += 1

    # w_id is the object id
    def count_O_w_num(self, w_id):
        if w_id not in self.O_w_num:
            self.O_w_num[w_id] = 0
        self.O_w_num[w_id] += 1

    # w_token is s,o
    def count_w_of_r_B(self, w_token):
        if w_token not in self.r_B_w_num:
            self.r_B_w_num[w_token] = 0
        self.r_B_w_num[w_token] += 1

    def load_triples(self):
        print("Start loading Triples.")
        with open(self.triple2idx_file, 'r', encoding="UTF-8") as f:
            all_triples = f.readlines()[1:]
            triple_num = len(all_triples)
            print("Num Of Triples: {}.".format(triple_num))
            self.total_e_num += triple_num * 2
            self.total_e_r_num += triple_num * 2
            self.total_s_o_num += triple_num * 1
            self.total_s_num += triple_num * 1
            self.total_o_num += triple_num * 1

            for line in all_triples:
                h, t, r = [int(w) for w in line.split()]

                self.count_U_w_num(h)
                self.count_U_w_num(t)
                self.count_w_of_e_B("{},{}".format(t, r))
                self.count_w_of_e_B("{},{}".format(h, r))
                self.count_S_w_num(h)
                self.count_O_w_num(t)
                self.count_w_of_r_B("{},{}".format(h, t))

                self.add_U_e_w(h, t)
                self.add_U_e_w(t, h)
                self.add_B_e_w(h, "{},{}".format(t, r))
                self.add_B_e_w(t, "{},{}".format(h, r))
                self.add_S_r_w(r, h)
                self.add_O_r_w(r, t)
                self.add_B_r_w(r, "{},{}".format(h, t))
        print("Finish Loading Triples.")

    def getLM(self):
        print("Start Calculating LM")

        def change_num2ratio(every_num_dict, total_num_dict):
            for key_id in every_num_dict:
                for w_id in every_num_dict[key_id]:
                    every_num_dict[key_id][w_id] = every_num_dict[key_id][w_id] / total_num_dict[key_id]

        change_num2ratio(self.U_e_w_num, self.U_e_num)
        change_num2ratio(self.B_e_w_num, self.B_e_num)

        change_num2ratio(self.S_r_w_num, self.S_r_num)
        change_num2ratio(self.O_r_w_num, self.O_r_num)
        change_num2ratio(self.B_r_w_num, self.B_r_num)

        def change_num2ratio_1(every_num_dict, total_num):
            for w_id in every_num_dict:
                every_num_dict[w_id] = every_num_dict[w_id] / total_num

        change_num2ratio_1(self.U_w_num, self.total_e_num)
        change_num2ratio_1(self.e_B_w_num, self.total_e_r_num)
        change_num2ratio_1(self.S_w_num, self.total_s_num)
        change_num2ratio_1(self.O_w_num, self.total_o_num)
        change_num2ratio_1(self.r_B_w_num, self.total_s_o_num)

    def get_jsd(self, p_dict, q_dict, prob_mode):
        # key_differ_num = abs(len(p_dict.keys()) - len(q_dict.keys()))
        # if key_differ_num >= js_key_differ_num_threshold:
        #     print("p: {}, q: {}, differ {}.".format(len(p_dict.keys()), len(q_dict.keys()), key_differ_num))
        # return 1

        merged_key_set = p_dict.keys() | q_dict.keys()

        # p_key_differ_num = abs(len(p_dict.keys()) - len(merged_key_set))
        # q_key_differ_num = abs(len(q_dict.keys()) - len(merged_key_set))
        # if p_key_differ_num > num_threshold_after_merging or q_key_differ_num > num_threshold_after_merging:
        #     print("p: {}, q: {}, megerd: {}.".format(len(p_dict.keys()), len(q_dict.keys()), len(merged_key_set)))
        #     print("p differ: {}, q differ {}.".format(p_key_differ_num, q_key_differ_num))
        # return 1

        def add_one_prob(tar_key, prob_dict, tar_prob_list):
            if tar_key in prob_dict:
                tar_prob_list.append(prob_dict[tar_key])
            else:
                if prob_mode == 0:  # entity Unigram
                    tar_prob_list.append(self.U_e_num[tar_key])
                if prob_mode == 1:  # entity Bigram
                    tar_prob_list.append(self.e_B_w_num[tar_key])
                if prob_mode == 2:  # relation Subject
                    tar_prob_list.append(self.S_w_num[tar_key])
                if prob_mode == 3:  # relation Object
                    tar_prob_list.append(self.O_w_num[tar_key])
                if prob_mode == 4:  # relation Bigram (Subject, Object)
                    tar_prob_list.append(self.r_B_w_num[tar_key])

        p_prob_list = []
        q_prob_list = []

        for key in merged_key_set:
            add_one_prob(key, p_dict, p_prob_list)
            add_one_prob(key, q_dict, q_prob_list)

        def jsd(p, q):
            p = np.array(p)
            q = np.array(q)
            p /= p.sum()
            q /= q.sum()
            m = (p + q) / 2
            return (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2

        return jsd(p_prob_list, q_prob_list)

    def load_e_r_dict(self):
        print("Load e2idx_file and r2idx_file.")
        with open(self.e2idx_file, 'r', encoding="UTF-8") as f:
            for line in f.readlines()[1:]:
                name, idx = line.split()
                idx = int(idx)
                self.e_name2idx[name] = idx
                self.e_idx2name[idx] = name
        with open(self.r2idx_file, 'r', encoding="UTF-8") as f:
            for line in f.readlines()[1:]:
                name, idx = line.split()
                idx = int(idx)
                if idx % 2 == 0:
                    self.r_name2idx[name] = idx
                    self.r_idx2name[idx] = name
        print("Finish loading e2idx_file and r2idx_file.")

    def get_top_K_simi_entity(self, p_e_name, result_file):

        if p_e_name not in self.e_name2idx:
            print("{} is not a valid name.".format(p_e_name))
            return
        print("Get top {} similar entities of entity '{}'.".format(js_top_k, p_e_name))

        result_dict = {}
        p_e_idx = self.e_name2idx[p_e_name]
        U_p_dict = self.U_e_w_num[p_e_idx]
        B_p_dict = self.B_e_w_num[p_e_idx]
        for cnt, q_e_idx in enumerate(self.e_idx2name.keys()):
            print("{}/{}. Calculating Simi Between {} and {}."
                  .format(cnt + 1, len(self.e_idx2name.keys()), p_e_name, self.e_idx2name[q_e_idx]))
            if q_e_idx == p_e_idx:
                continue
            U_q_dict = self.U_e_w_num[q_e_idx]
            U_jsd = self.get_jsd(U_p_dict, U_q_dict, 0)

            B_q_dict = self.B_e_w_num[q_e_idx]
            B_jsd = self.get_jsd(B_p_dict, B_q_dict, 1)

            weighted_jsd = alpha * U_jsd + (1 - alpha) * B_jsd
            if weighted_jsd < 0.5:
                result_dict[q_e_idx] = weighted_jsd

            if (cnt + 1) % 10000 == 0:
                sorted_result_list = sorted(result_dict.items(), key=lambda kv: kv[1])[:js_top_k * 5]
                with open(result_file, 'w', encoding="UTF-8") as f:
                    for s_res in sorted_result_list:
                        f.write("{}\t{}\n".format(self.e_idx2name[s_res[0]], s_res[1]))

            print("JSD: U: {}, B: {}, Weighted: {}.".format(U_jsd, B_jsd, weighted_jsd))

        sorted_result_list = sorted(result_dict.items(), key=lambda kv: kv[1])[:js_top_k * 5]
        with open(result_file, 'w', encoding="UTF-8") as f:
            for s_res in sorted_result_list:
                f.write("{}\t{}\n".format(self.e_idx2name[s_res[0]], s_res[1]))

    def get_top_K_simi_relation(self, p_r_name, result_file):
        if p_r_name not in self.r_name2idx:
            print("{} is not a valid name.".format(p_r_name))
            return
        print("Get top {} similar relation of relation '{}'.".format(js_top_k, p_r_name))

        result_dict = {}
        p_r_idx = self.r_name2idx[p_r_name]
        S_p_dict = self.S_r_w_num[p_r_idx]
        O_p_dict = self.O_r_w_num[p_r_idx]
        B_p_dict = self.B_r_w_num[p_r_idx]

        for cnt, q_r_idx in enumerate(self.r_idx2name.keys()):
            if q_r_idx == p_r_idx:
                continue
            print("{}/{}. Calculating Simi Between {} and {}."
                  .format(cnt + 1, len(self.r_idx2name.keys()), p_r_name, self.r_idx2name[q_r_idx]))

            S_q_dict = self.S_r_w_num[q_r_idx]
            S_jsd = self.get_jsd(S_p_dict, S_q_dict, 2)

            O_q_dict = self.O_r_w_num[q_r_idx]
            O_jsd = self.get_jsd(O_p_dict, O_q_dict, 3)

            B_q_dict = self.B_r_w_num[q_r_idx]
            B_jsd = self.get_jsd(B_p_dict, B_q_dict, 4)

            weighted_jsd = miu_s * S_jsd + miu_o * O_jsd + (1 - miu_s - miu_o) * B_jsd
            result_dict[q_r_idx] = weighted_jsd

            # print("JSD: S: {}, O: {}, B: {}, Weighted: {}."
            #       .format(S_jsd, O_jsd, B_jsd, weighted_jsd))

        sorted_result_list = sorted(result_dict.items(), key=lambda kv: kv[1])[:js_top_k]
        with open(result_file, 'w', encoding="UTF-8") as f:
            for s_res in sorted_result_list:
                f.write("{}\t{}\n".format(self.r_idx2name[s_res[0]], s_res[1]))

    def pre_process_data(self):
        self.load_triples()
        self.load_e_r_dict()
        self.getLM()


def search_manual():
    file_path_dict = {}
    with open("./file_path_store.txt", 'r', encoding="UTF-8") as f:
        for line in f.readlines():
            key_name, file_path = line.split()
            file_path_dict[key_name] = file_path

    folder = file_path_dict["folder"]
    e2idx_shortcut_file = folder + file_path_dict["e2idx_shortcut_file"]
    # add inverse relation
    r2idx_shortcut_file = folder + file_path_dict["r2idx_shortcut_file"]
    triple2idx_file = folder + file_path_dict["triple2idx_file"]

    result_folder = file_path_dict["result_folder"]
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    simiGraph = SimiGraph(triple2idx_file, e2idx_shortcut_file, r2idx_shortcut_file)
    simiGraph.pre_process_data()

    while True:
        mode = input("Choose mode: ")
        if mode == "end":
            break
        elif mode == "e":
            my_input = input("Please input entity: ")
            result_file = result_folder + my_input.split(":")[-1] + ".txt"
            if os.path.exists(result_file):
                print("{} already exists.".format(result_file))
                continue
            simiGraph.get_top_K_simi_entity(my_input, result_file)
        elif mode == "r":
            my_input = input("Please input relation: ")
            result_file = result_folder + my_input.split(":")[-1] + ".txt"
            if os.path.exists(result_file):
                print("{} already exists.".format(result_file))
                continue
            simiGraph.get_top_K_simi_relation(my_input, result_file)


def search_bunch():
    file_path_dict = {}
    with open("./file_path_store.txt", 'r', encoding="UTF-8") as f:
        for line in f.readlines():
            key_name, file_path = line.split()
            file_path_dict[key_name] = file_path

    folder = file_path_dict["folder"]
    e2idx_shortcut_file = folder + file_path_dict["e2idx_shortcut_file"]
    # add inverse relation
    r2idx_shortcut_file = folder + file_path_dict["r2idx_shortcut_file"]
    triple2idx_file = folder + file_path_dict["triple2idx_file"]

    result_folder = file_path_dict["result_folder"]
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    simiGraph = SimiGraph(triple2idx_file, e2idx_shortcut_file, r2idx_shortcut_file)
    simiGraph.pre_process_data()

    # entity_list = ["dbr:Paris","dbr:Amazon.com","dbr:Jeep_Wrangler"]
    entity_list = ["dbr:Amazon.com"]

    for e_name in list(set(entity_list)):
        print("Get similar entities of E: {}.".format(e_name))
        result_file = result_folder + e_name.split(":")[-1] + ".txt"
        if os.path.exists(result_file):
            print("{} already exists.".format(result_file))
            continue
        with open(result_file, 'w', encoding="UTF-8") as f:
            f.write("Test\n")
        simiGraph.get_top_K_simi_entity(e_name, result_file)


if __name__ == "__main__":
    # search_manual()
    search_bunch()
