# coding=utf-8
from __future__ import division

import json
import itertools
from tabulate import tabulate

from collections import defaultdict

json_path="../../data/Images/output.json"
OUTPUT_PATH="../rules.basket"

"""
data of form:

[
    {
    "name":name,
        "works":
        [
            {
            "path":path
            "rules":
                {
                "supp":support,
                "conf":confidence
                "lift":lift,
                "cove":coverage,
                "leve":leverage,
                "antecedent":antecedent,
                "consequent":consequent
                }
            }
        ]
    }
]
"""

def bin(number):
    return (int(number*10))/10.+0.05

def compose_rule(rule):
    # print(rule["antecedent"])
    s=u" ".join(rule["antecedent"])+'->'+" ".join(rule["consequent"])
    return s.replace(',',' ')

def compare_rule(rule1,rule2):
    return rule1["antecedent"]==rule2["antecedent"] and rule1["consequent"]==rule2["consequent"]

def make_row(artist,rule):
    return artist.replace(u'\xed',"i")+","+compose_rule(rule)+' '+str(bin(rule["conf"]))+'\n'

def generate_artist_dct_lines(artist_dct):
    artist=artist_dct["name"]
    # print(artist_dct["works"][0].keys())
    rules=[work["rules"] for work in artist_dct["works"]]
    # print(len(rules))
    return map(lambda rule:make_row(artist,rule),itertools.chain(*rules))

def line_generator(data):
    return itertools.chain(*map(generate_artist_dct_lines,data))

def process_data(data,output_path=OUTPUT_PATH):
    with open(output_path,'w') as f:
        map(f.write,line_generator(data))

def psuedo_association_rules(data):
    rule_lookup=defaultdict(lambda:{})
    results={}
    for artist_dct in data:
        occurrences=defaultdict(lambda:0)
        works=list(map(lambda work: work["rules"],artist_dct["works"]))
        fraction=1./len(works)
        for work in works:
            for rule in work:
                rule_lookup[artist_dct["name"]][compose_rule(rule)]=rule
                occurrences[compose_rule(rule)]+=fraction
        results[artist_dct["name"]]=occurrences
    return results,rule_lookup

def analyze_psuedo_association_rules(psuedo_association_rules_results, threshold=0.3):
    number_artists=float(len(psuedo_association_rules_results.keys()))
    average_occurrences=defaultdict(lambda:0)
    rules=set.union(*map(set,(occurrences for _,occurrences in psuedo_association_rules_results.items())))
    for rule in rules:
        total=sum([occurrences[rule] for _,occurrences in psuedo_association_rules_results.items()])
        average_occurrences[rule]=total/number_artists

    interesting_rules=defaultdict(lambda:[])
    for artist,occurrences in psuedo_association_rules_results.items():
        for rule in rules:
            difference=abs(occurrences[rule]-average_occurrences[rule])
            if difference>threshold:
                interesting_rules[artist].append([rule,difference])

    return interesting_rules

def print_interesting_rules(interesting_rules,rule_lookup,include=('conf','supp','lift'),only_first=False):
    for artist,rules in interesting_rules.items():
        artist=artist.replace(u'\xed',"i")
        rules.sort(key=lambda rule:rule[1],reverse=True)
        if only_first:
            rules=rules[:only_first]
        for additional in include:
            for rule in rules:
                try:
                    rule.append(rule_lookup[artist][rule[0]][additional])
                except KeyError:
                    rule.append('N/A')
        print('\n\n{}\n'.format(artist))
        print(tabulate(rules,headers=['Rule','Difference from Average']+list(include)))

if __name__ == '__main__':
    with open(json_path,'r') as j:
        data=json.load(j)

    # process_data(data)
    results, rule_lookup=psuedo_association_rules(data)
    print_interesting_rules(analyze_psuedo_association_rules(results,threshold=0.2),rule_lookup,only_first=10)