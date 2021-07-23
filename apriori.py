import psycopg2 as pg2
import itertools


class Apriori:

    def __init__(self):
        self.database_file = list()
        self.csv_file = None
        self.goods_sale_with_date = list()
        self.goods_sale_without_date = list()
        self.assoc_rules = list()
        self.product_string = list()
        self.product_id = list()
        self.length_csv_file = 0

    def database_connection(self):
        conn = pg2.connect(database='SmartSolution', user='postgres', password='password')
        cur = conn.cursor()
        cur.execute('select * from goods')
        goods_dataset = cur.fetchall()

        for i in goods_dataset:
            self.database_file.append([int(i[0]), str(i[1]).strip(), int(i[2]), int(i[3]),str(i[4]).strip()])
            self.product_id.append(str(i[0]))

    def sales_data(self):
        goods_file = 'Sales.csv'
        with open(goods_file, "r") as goods_file:
            goods_file = goods_file.read().split('\n')

        self.csv_file = [line.split(',') for line in goods_file]
        self.length_csv_file = len(self.csv_file) - 1

    def from_to(self, date_from, date_to):
        self.database_connection()
        self.sales_data()
        date_from = date_from.split('/')
        date_to = date_to.split('/')
        flag = False
        for i in range(self.length_csv_file):
            date, month, year = self.csv_file[i][0].split('/')
            if int(date + month) == int(date_from[0] + date_from[1]):
                for j in range(i, self.length_csv_file):
                    date1, month1, year1 = self.csv_file[j][0].split('/')
                    if int(date1 + month1) == int(str(int(date_to[0]) + 1) + date_to[1]):
                        flag = True
                        break
                    else:
                        self.goods_sale_without_date.append(self.csv_file[j][1:])
                        self.goods_sale_with_date.append(self.csv_file[j])
            if flag:
                break

    def support(self, itemset):
        temp = self.goods_sale_without_date
        for i in itemset:
            temp = [item for item in temp if i in item]
        return len(temp) / len(self.goods_sale_without_date)

    def aprioriiteration(self, combination, min_support, min_confidence):
        min_support = min_support / 100
        min_confidence = min_confidence / 100
        product_set = list(itertools.combinations(self.product_id, combination))
        for itemset in product_set:
            if self.support(itemset) >= min_support:
                for j in range(combination):
                    rule_to = itemset[j]
                    rule_from = [x for x in itemset if x != itemset[j]]
                    confidence = self.support(itemset) / self.support(rule_from)
                    if confidence >= min_confidence:
                        self.assoc_rules.append((rule_from, rule_to))

    def int_to_string(self):

        for i in self.assoc_rules:
            temp1 = []
            temp2 = []
            for j in i[0]:
                for k in range(len(self.database_file)):
                    if str(self.database_file[k][0]) == j:
                        temp1.append(self.database_file[k][1])
                        break

            for k in range(len(self.database_file)):
                if str(self.database_file[k][0]) == i[1]:
                    temp2.append(self.database_file[k][1])
                    break
            self.product_string.append((temp1, temp2[0]))

        temp = ''
        for i in range(len(self.product_string)):
            temp += str(i) + '  ' + str(self.product_string[i]) + '\n'

        return temp


if __name__ == '__main__':
    a = Apriori()
    a.from_to('1/02/2020', '23/04/2020')
    #a.aprioriiteration(3, 1.5, 35)
    #print(a.int_to_string())
    print(a.database_file)