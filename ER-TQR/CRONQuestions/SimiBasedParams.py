import mysql.connector

# mydb = mysql.connector.connect(
#     host='localhost',
#     user="root",
#     password="3721",
#     auth_plugin="mysql_native_password",
#     database="kg")
#
# mydb = mysql.connector.connect(
#         host='114.212.86.67',
#         user="xzlyu",
#         password="123456",
#         auth_plugin="mysql_native_password",
#         database="kg")

"""
Unigram ration
"""
alpha = 0.75

"""
Subject ration for relation
"""
miu_s = 0.4

"""
Object ration for relation
"""
miu_o = 0.4

"""
Before computing js-divergence, compare the num of keys of two distribution,
cancel this calculation if they differ much.
"""
js_key_differ_num_threshold = 2000

"""
After merging the keys of two distribution,
threshold for the difference between the size of merged key set and original key set
"""
num_threshold_after_merging = 1000

"""
number of top kl value entities to reserve
"""
js_top_k = 5
