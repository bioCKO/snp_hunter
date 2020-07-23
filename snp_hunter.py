#!/usr/bin/env python3

"""Hunt for sex-specific transcripts in male/female assemblies."""

import fasta
import subprocess

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')


candidates = []  # (CID, CID) from (male, female) assembly
male_hepato = fasta.read("hp_male_trinity.fasta")
female_hepto = fasta.read("hp_female_trinity.fasta")

for cid, nts in female_hepato.items():
    # BLAST search against male assembly
    # Expect a hit with near 100% identity. Shall we say... 99.9%?
    # => Is there also a hit with lower identity that could be a male allele?
    #     => Is it full of SNPs (rather than a splice variant)?
    #         => BLAST search it back against F assembly (out = CID_M_CID_F.xml)
    #         => If there is no better hit than this one, append to candidates
    #            (It's male specific but accompanied by a female allele)
    # else delete blastout.xml

for candidate in candidates:
    # M_cid, F_cid = candidate
    # Get cds + protein for each
    # If protein conservation greater than cds, we have synonymous mutations
    # Store => M_cid, F_cid, cDNA length, CDS length, Pep length, UTR SNPs, CDS SNPs, synonymous SNPs

# ==> Filter and observe
