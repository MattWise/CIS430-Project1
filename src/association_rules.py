import Orange
import argparse

def get_rules(basket_path, support=0.1, confidence=None):
    data = Orange.data.Table(basket_path)
    kwargs={'support':support}
    if confidence is None:
        kwargs['confidence']=confidence
    return Orange.associate.AssociationRulesSparseInducer(data, **kwargs)

def print_rules(rules):
    Orange.associate.sort(rules,ms=['confidence'])
    Orange.associate.print_rules(rules,ms=['support','confidence','lift','coverage','leverage'])

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Extract rules from .basket and print the results")
    parser.add_argument("basket",type=str,help=".basket to process")
    parser.add_argument("-s",'--support', type=float, help="Minimum support",default=0.3)
    args=parser.parse_args()

    print_rules(get_rules(args.basket,support=args.support))