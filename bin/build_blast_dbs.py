#!/usr/bin/env python3

"""Build BLAST databases from all FASTA files in data/.

Protein FASTA file names must end in "_pep.*" to be processed correctly.
"""

import os
import subprocess

data_path = '../data/'
db_path = '../blast/db/'

FASTA_EXTS = [
    'fa',
    'fas',
    'fsa',
    'fasta',
]

for f in os.listdir(data_path):
    base, ext = f.rsplit('.', 1)
    if ext not in FASTA_EXTS:
        continue
    if base.endswith("_pep"):
        dbtype = "prot"
    else:
        dbtype = "nucl"
    args = [
        "makeblastdb",
        "-in", os.path.join(data_path, f),
        "-out", os.path.join(db_path, f),
        "-dbtype", dbtype,
        "-parse_seqids",
    ]
    subprocess.run(args, check=True)

print('\nBLAST databases built successfully\n')
