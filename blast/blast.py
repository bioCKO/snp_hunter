"""A wrapper for the NCBI BLAST tool."""

import os
import uuid
import logging
import subprocess
from .parse import BlastResult

logger = logging.getLogger('root')


def blast(algorithm, queryfile, db):
    """Run a blast search, check outcome and return parsed result."""
    name = os.path.basename(queryfile)
    outfilename = 'blast/blastout_%s.xml' % name.rsplit('.', 1)[0]

    if not (os.path.exists(f"{ db }.nhr") or os.path.exists(f"{ db }.phr")):
        raise FileNotFoundError(f'No BLAST DB found for "{ db }"')
    if not os.path.exists(queryfile):
        raise FileNotFoundError(f'Query file "{ queryfile }" not found')

    args = (
        algorithm,
        '-db', db,
        '-query', queryfile,
        '-out', outfilename,
        '-outfmt', '5',
        "-evalue", '1E-50',
        "-max_target_seqs", '10',
        "-num_threads", '50',
    )
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stderr)
        raise exc

    return outfilename


def pairwise_blast(algorithm, query, subject):
    """BLAST align two sequences and return BlastResult instance."""
    queryfile = os.path.join('blast', uuid.uuid4().hex + ".fas")
    subjectfile = os.path.join('blast', uuid.uuid4().hex + ".fas")
    outfile = os.path.join('blast', uuid.uuid4().hex + ".xml")

    with open(queryfile, 'w') as f:
        f.write(">CDS_query\n" + query)
    with open(subjectfile, 'w') as f:
        f.write(">CSD_subject\n" + subject)

    args = (
        algorithm,
        '-query', queryfile,
        '-subject', subjectfile,
        '-out', outfile,
        '-outfmt', '5',
        "-max_target_seqs", '10',
    )
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stderr)
        raise RuntimeError(exc.stderr)
    finally:
        os.remove(queryfile)
        os.remove(subjectfile)
    return BlastResult(outfile)
