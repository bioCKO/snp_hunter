#!/usr/bin/env python3

"""Hunt for sex-specific transcripts in male/female assemblies."""

import fasta
from blast import blast

import logging
import logging.config
logging.config.fileConfig('logging/log.conf')
logger = logging.getLogger('root')


# Output file header
header = ','.join([
    'Contig_id',
    'E-value',
    'Bitscore',
    'Identities',
    'Positives',
    'Align length',
    'Q-cover %',
])

# Sequences to use as BLAST queries
male_specific_500 = fasta.read("data/top500.fas")

# BLAST params
algorithm = 'tblastn'
dbpath = 'blast/db/F_HP_pep.fas'

try:
    csv = open('output.csv', 'a+')
    csv.write(header + '\n')

    for cid, nts in male_specific_500.items():
        # Perform BLAST search -> all hits saved in blastout_*.xml in blast/
        # Blastout.xml files can be read again in future with parse.BlastResult
        result = blast(algorithm, cid, nts, dbpath)
        hit = result.hit[0]
        hsp = result.hit[0].hsp[0]
        line = ','.join([
            hit.contig_id,
            str(hsp.evalue),
            str(round(hsp.bitscore)),
            str(hsp.identities),
            str(hsp.positives),
            str(hsp.length),
            str(round(hsp.query_cover)),
        ])
        csv.write(line + '\n')
finally:
    csv.close()

    """
    What are we looking for?
    => Is it full of SNPs (rather than a splice variant)?
    => BLAST back against male assembly
        => Is there a higher identity hit could be an X allele?
    """

# %% Round 2

# candidates = []  # (CID, CID) from (male, female) assembly
# female_hp = fasta.read("data/F_HP_pep.fas")

# for candidate in candidates:
    # M_cid, F_cid = candidate
    # Get cds + protein for each
    # If protein conservation greater than cds, we have synonymous mutations
    # CSV <= [M_cid, F_cid, cDNA length, CDS length,
    #           Pep length, UTR SNPs, CDS SNPs, synonymous SNPs]
    # pass

# ==> Filter and observe
