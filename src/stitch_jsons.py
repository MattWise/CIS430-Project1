import argparse

OUTPUT_PATH=r"./output.json"

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Extract rules from .basket and print the results")
    parser.add_argument("baskets",type=str,help=".baskets to process",nargs="+")
    parser.add_argument("-o", '--output', type=str, help="Output File Path", default=None)

    args=parser.parse_args()

    # output_path=args.output
    # if output_path is None:
    #     output_path=generate_output_name(args.basket,extension='_rules.json')



    for basket in args.baskets:
        output_path = generate_output_name(basket, extension='_rules.json')
        save_rules_to_json(get_rules(basket,support=args.support),output_path)