#!/usr/bin/env python3
"""Run a test to ensure everything is working ok."""

import fasta
import blast

input("""
This test requires that the following are accessible from the project root:

Assembly:   data/top500_M_reads.fas
BLAST DB:   blast/db/f_hp.fas
Program:    blastn

""")

algorithm = 'blastn'
database = 'blast/db/f_hp.fas'
fas = fasta.read('data/top500_M_reads.fas')

for k, v in fas.items():
    result = blast.blast(
        algorithm,
        k, v,
        database,
    )
    break

print("Test blast results:")
print(result.report())
