#!/usr/bin/env python
import os
import pymol
from pymol import cmd


def get_args():
    desc = "generate mutation with pymol."
    try:
        parser = argparse.ArgumentParser(
            description=desc, formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument(
            "pdbfile",
            action="store",
            help="File of original structures (pdb only).",
        )
        parser.add_argument(
            "mutation_file",
            action="store",
            help='File of mutation mappings like so: "SeqID,X123Y"',
        )
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            exit(1)
    except:
        sys.stderr.write(
            "An exception occurred with argument parsing. Check your provided options.\n"
        )

    return parser.parse_args()



class Mutation(object):
    """A class wrapper for sequence IDs so that duplicate IDs"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "'" + self.name + "'"

    def __str__(self):
        return self.name


def get_seq(fa:str): 
    records = list(SeqIO.parse(fa, "fasta"))
    seqs = []
    for i in range(len(records)):
        seqs.append(records[i].seq)
    
    return seqs


def pdb_to_fasta(pdb_id: str):
    os.system(f'python pdb2fasta.py {pdb_id}.pdb > {pdb_id}.fasta')
    return print("start to convert pdb to fasta")

def parse_mapfile(mapfile: str):
    """Return a dict of mapped mutations.
    File should resemble:
    SequenceID,A123B
    SequenceID2,X234Y
    Sequence IDs should exactly match the fasta headers, as parsed by BioPython.
    """
    with open(mapfile, "r") as handle:
        mut_dict = OrderedDict()
        for line in handle:
            id, change = line.lstrip(">").rstrip("\n").split(",")
            mut_dict[Mutation(id)] = change
    
    for k, v in mut_dict.items():
        assert v[0].isalpha(), (
            "First character of mutation map is not a valid letter. Got: %s" % v[0]
        )
        assert v[-1].isalpha(), (
            "Last character of mutation map is not a valid letter. Got: %s" % v[-1]
        )
        assert v[1:-1].isdigit(), (
            "Location string of mutation map is not a valid number. Got: %s" % v[1:-1]
        )

    return mut_dict


def get_mutation_map(s1:list, s2:list):
    mut_flag = set()
    for i, aa in enumerate(zip(s1, s2)):
        if aa[0] != aa[1]:
            flag = str(aa[0])+str(i+1)+str(aa[1])
            mut_flag.add(flag)

    return mut_flag


def get_pdb_id(pdbfile):
    return pdbfile.split('.')[0]


def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1.upper(), s2.upper()))


def main():
    args = get_args()
    pdb1 = args.pdbfile1
    pdb2 = args.pdbfile2
    pdb_id1 = get_pdb_id(pdb1)
    pdb_id2 = get_pdb_id(pdb2)
    pdb_to_fasta(pdb_id1)
    pdb_to_fasta(pdb_id2)
    fa = f'{pdb_id1}.fasta'
    fa2 = f'{pdb_id2}.fasta'
    mutations = parse_mapfile(args.mutation_file)

    for i in range(len(get_seq(fa))):
        mut_flag = []
        mut_flag.append(get_mutation_map(get_seq(fa2)[i], get_seq(fa)[i]))
        print(mut_flag)

    #for j in mutations.values():
if __name__ == "__main__":
    main()
