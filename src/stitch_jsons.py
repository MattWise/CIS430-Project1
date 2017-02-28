import os
import argparse
import json

"""
Stitched json of form:

[
    {
    "name":name,
        "works":
        [
            {
            "path":path
            "rule":
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

OUTPUT_PATH = r"./output.json"


def get_object_from_json(json_path):
    with open(json_path, 'r') as j:
        return json.load(j)


def get_artist(json):
    return os.path.basename(os.path.dirname(json))


def is_json(json_path):
    return os.path.splitext(json_path)[1] == ".json"


def stitch_jsons(jsons, output_path=OUTPUT_PATH):
    jsons = map(os.path.abspath, jsons)
    assert all(map(is_json, jsons))

    artists={get_artist(j):[] for j in jsons}
    for j in jsons:
        artists[get_artist(j)].append(j)

    new_list = []
    for artist,json_paths in artists.items():
        works=[]
        for json_path in json_paths:
            work={"rules":get_object_from_json(json_path),"path":os.path.basename(json_path)}
            rules=get_object_from_json(json_path)
            work["path"]=os.path.basename(json_path)
            works.append(work)
        new_list.append({"name":artist,"works":works})
    with open(output_path, 'w') as j:
        json.dump(new_list, j)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stitch several *_rules.json files together into one json.")
    parser.add_argument("jsons", type=str, help=".json files to process", nargs="+")
    parser.add_argument("-o", '--output', type=str, help="Output File Path", default=OUTPUT_PATH)

    args = parser.parse_args()

    stitch_jsons(args.jsons, output_path=args.output)
