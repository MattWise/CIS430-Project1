import Orange
import argparse
import json
import os
import re

import utilities
import process_image

def get_rules(basket_path, support=0.3, confidence=None):
    data = Orange.data.Table(basket_path)
    if confidence is None:
        return Orange.associate.AssociationRulesSparseInducer(data, support=support,max_item_sets=1000000)
    else:
        return Orange.associate.AssociationRulesSparseInducer(data, support=support, confidence=confidence,max_item_sets=100000000)

def print_rules(rules):
    Orange.associate.sort(rules,ms=['confidence'])
    Orange.associate.print_rules(rules,ms=['support','confidence','lift','coverage','leverage'])

def get_rules_from_image(img_path,size_pixel=process_image.SIZE_PIXEL,number_bins=process_image.NUMBER_BINS,support=0.1,prnt=False):
    basket_path=r'./tmp.basket'
    process_image.make_basket(img_path=img_path,
                              size=utilities.extract_size(img_path),
                              size_pixel=size_pixel,
                              number_bins=number_bins,
                              output_file=basket_path,
                              block_size=16)
    rules=get_rules(basket_path=basket_path,support=support)
    if prnt:
        print_rules(rules)
    return rules

def string_to_array(s):
    return re.sub(r'\[\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*\]',r'[\1,\2,\3]',s)

def get_arrays(string):
    left_brackets=[i for i,x in enumerate(string) if x=="["]
    right_brackets = [i for i, x in enumerate(string) if x == "]"]
    assert len(left_brackets)==len(right_brackets)
    for left_bracket,right_bracket in zip(left_brackets,right_brackets):
        yield string[left_bracket:right_bracket+1]

def parse_rule(rule):
    implies_symbol=r'->'
    split_index=rule.find(implies_symbol)

    antecedent=rule[:split_index]
    consequent=rule[split_index:]

    antecedent=list(map(string_to_array,get_arrays(antecedent)))
    consequent = list(map(string_to_array, get_arrays(consequent)))

    return antecedent,consequent

def generate_output_name(path,extension='_rules.json'):
    return os.path.splitext(path)[0]+extension

def save_rules_to_json(rules,output_path):
    rules_object=[]
    for r in rules:
        antecedent, consequent=parse_rule(str(r))
        rules_object.append({"supp":r.support, "conf":r.confidence, "lift":r.lift, "cove":r.coverage, "leve":r.leverage, "antecedent":antecedent,"consequent":consequent})
    with open(output_path,mode='w') as f:
        json.dump(rules_object,f)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Extract rules from .basket and print the results")
    parser.add_argument("baskets",type=str,help=".baskets to process",nargs="+")
    parser.add_argument("-s",'--support', type=float, help="Minimum support",default=0.1)
    parser.add_argument("-c", '--confidence', type=float, help="Minimum confidence", default=None)
    #parser.add_argument("-o", '--output', type=str, help="Output File Path", default=None)

    args=parser.parse_args()

    # output_path=args.output
    # if output_path is None:
    #     output_path=generate_output_name(args.basket,extension='_rules.json')



    # for basket in args.baskets:
    #     output_path = generate_output_name(basket, extension='_rules.json')
    #     save_rules_to_json(get_rules(basket,support=args.support),output_path)

    for basket in args.baskets:
        output_path = generate_output_name(basket, extension='_rules.txt')
        print('\n\n{}'.format(os.path.basename(output_path)))
        print_rules(get_rules(basket,support=args.support,confidence=args.confidence))


