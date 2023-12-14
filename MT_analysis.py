import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='MT Analysis')
    parser.add_argument('-f', '--filename', required=True)
    args = parser.parse_args()
    data = []
    with open(args.filename, 'r')as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    print(f'DRAWN DATA FROM {args.filename} counting transformation')
    data = [x[2] for x in data]
    transformer_count = {'addcomment': 0, 
                         'addneutral': 0,
                         'addvar': 0,
                         'forone': 0,
                         'iffalseelse': 0,
                         'iftrue': 0,
                         'lambdaidentity': 0,
                         'renameparam': 0,
                         'renamevar': 0,
                         'whiletrue': 0,
                         }
    data = [s.split(',') for s in data]
    for s in data:
        for t in s:
            match t:
                case 'AddVariableTransformer':
                    transformer_count['addvar']+=1
                case 'AddCommentTransformer':
                    transformer_count['addcomment']+=1
                case 'RenameVariableTransformer':
                    transformer_count['renamevar']+=1
                case 'RenameParameterTransformer':
                    transformer_count['renameparam']+=1
                case 'LambdaIdentityTransformer':
                    transformer_count['lambdaidentity']+=1
                case 'AddNeutralElementTransformer':
                    transformer_count['addneutral']+=1
                case 'IfTrueTransformer':
                    transformer_count['iftrue']+=1
                case 'IfFalseElseTransformer':
                    transformer_count['iffalseelse']+=1
                case 'ForOneTransformer':
                    transformer_count['forone']+=1
                case 'WhileTrueTransformer':
                    transformer_count['whiletrue']+=1
    for k in transformer_count.keys():
        print(f'{k} : {transformer_count[k]}')

