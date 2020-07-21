import os
import nltk
from nltk import grammar, parse
from nltk.sem import chat80

class nl_to_sql():
    def __init__(self):
        self.sql_grammar = """
                            % start S
                            S[SEM=(?np + WHERE + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]
                            VP[SEM=(?v + ?pp)] -> IV[SEM=?v] PP[SEM=?pp]
                            VP[SEM=(?v + ?ap)] -> IV[SEM=?v] AP[SEM=?ap]
                            NP[SEM=(?det + ?n)] -> Det[SEM=?det] N[SEM=?n]
                            PP[SEM=(?p + ?np)] -> P[SEM=?p] NP[SEM=?np]
                            AP[SEM=?pp] -> A[SEM=?a] PP[SEM=?pp]
                            NP[SEM='Country="greece"'] -> 'Greece' | 'greece'
                            NP[SEM='Country="africa"'] -> 'africa'
                            NP[SEM='Country="thailand"'] -> 'thailand'
                            NP[SEM='Country="china"'] -> 'China' | 'china'
                            Det[SEM='SELECT'] -> 'Which' | 'What' | 'which' | 'what'
                            N[SEM='City FROM city_table'] -> 'cities'
                            N[SEM='Population FROM city_table'] -> 'population'
                            IV[SEM=''] -> 'are'
                            IV[SEM=''] -> 'is'
                            A[SEM=''] -> 'located'
                            P[SEM=''] -> 'in'
                            """
        self.grammar = grammar.FeatureGrammar.fromstring(self.sql_grammar)
        self.parser = parse.FeatureEarleyChartParser(self.grammar)
        self.menu_display()
    
    def menu_display(self):
        print("NLP to SQL converter\n")
        print("1. Show only query \n")
        print("2. show query and execute it \n")
        print("3. Exit \n")
        self.choice = input("choice [1,2,3] : ")
        self.choice = int(self.choice)
        print("\n")
        self.switcher()

    def sql_only(self):
        self.query = input("Enter the Natural Language: ")
        self.trees = list(self.parser.parse(self.query.split()))
        self.answer = self.trees[0].label()['SEM']
        self.answer = [s for s in self.answer if s]
        self.q = ' '.join(self.answer)
        print("\n the Sql query is as follows \n")
        print(self.q)

    def sql_run(self):
        self.query = input("Enter the Natural Language: ")
        self.trees = list(self.parser.parse(self.query.split()))
        self.answer = self.trees[0].label()['SEM']
        self.answer = [s for s in self.answer if s]
        self.q = ' '.join(self.answer)
        print("\n the Sql query is as follows \n")
        print(self.q)
        print("\n Querry is running....")
        self.rows = chat80.sql_query('corpora/city_database/city.db', self.q)
        self.count = 0
        self.my_res = []
        for r in self.rows:
            self.my_res.append(r)
            self.count = self.count + 1
        if self.count is 0:
            print("no data found")
        else:
            for iter_var in range(self.count):
                temp_str = self.my_res[iter_var][0]
                print(temp_str)
            self.sum_er()
    
    def sum_er(self):
        try:
            self.x = int(str(self.my_res[0][0]))
        except ValueError as ve:
            print('No values to Total...Leaving...')
            self.x = -1
        if self.x > 0:
            print("Got some values to toatal ...")
            self.temp_counter =0 
            for iter_var in range(self.count):
                self.temp_counter = self.temp_counter + int(str(self.my_res[iter_var][0]))
            print("the total population is : ",self.temp_counter)

    def exit_prgm(self):
        print("\n Exiting")
        os._exit(os.EX_OK)

    def switcher(self):
        if self.choice == 1:
            self.sql_only()
        elif self.choice == 2:
            self.sql_run()
        elif self.choice ==3:
            self.exit_prgm()
        else:
            print("enter a valid choice")
            self.menu_display()
            
if __name__ == "__main__": 
	prgm = nl_to_sql() 