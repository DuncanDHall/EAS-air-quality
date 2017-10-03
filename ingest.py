# Functionize everything!
def load_split_file(file):
    with open(file) as f:
        lines1 = pd.DataFrame(f.readlines(),columns=['raw'])
    
    lines1['comment']=[s.startswith('#') for s in lines1.raw]
    lines1['type']=[s.split('|')[0] for s in lines1.raw]
    
    # Drop comment lines
    lines1.drop(lines1[lines1.comment].index, inplace=True)
    lines1.tail()
    
    # Split into row types
    types=lines1.type.unique()
    outputs = dict()
    for t in types:
        if t not in heads:
            raise Exception('Unknown row type '+t)
        outputs[t] = StringIO(heads[t]+'\n'+''.join(lines1[lines1.type==t].raw))

    return outputs