#!/usr/bin/env python3

"""Hunt for sex-specific transcripts in male/female assemblies."""

import fasta
from blast import blast

import logging
import logging.config
logging.config.fileConfig('logging/log.conf')
logger = logging.getLogger('root')

"""
Need to make:
    X M/F assemblies
    X Expression quantitation (bbmap)
    - BLAST DBs
    X BLAST XML Parser
    - CDS and protein (transdecoder)
    - CDS/protein BLAST DBs?
    - Perhaps domain annotations with CD-SEARCH?
"""

candidates = []  # (CID, CID) from (male, female) assembly
male_hepato = fasta.read("data/hp_male_trinity.fasta")
female_hepato = fasta.read("data/hp_female_trinity.fasta")

for cid, nts in female_hepato.items():
    # BLAST search against male assembly
    dbpath = 'data/hp_male_trinity.fasta'
    outfile = 'blast/blastout_F_%s.xml' % cid
    result = blast(cid, nts, dbpath, outfile)

    # Expect a hit with near 100% identity. Shall we say... 99.9%?
    # => Is there also a hit with lower identity that could be a male allele?
    #   => Is it full of SNPs (rather than a splice variant)?
    #     => BLAST search it back against F assembly (out = CID_M_CID_F.xml)
    #     => If there is no better hit than this one, append to candidates
    #        (It's male specific but accompanied by a female allele)
    #        & PKL <= parsed blastout
    # else delete blastout.xml
    pass

for candidate in candidates:
    # M_cid, F_cid = candidate
    # Get cds + protein for each
    # If protein conservation greater than cds, we have synonymous mutations
    # CSV <= [M_cid, F_cid, cDNA length, CDS length,
    #           Pep length, UTR SNPs, CDS SNPs, synonymous SNPs]
    pass

# ==> Filter and observe
