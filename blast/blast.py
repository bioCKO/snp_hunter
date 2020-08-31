"""A wrapper for the NCBI BLAST tool."""

import os
import logging
import subprocess

logger = logging.getLogger('root')


def blast(algorithm, queryfile, db):
    """Run a blast search, check outcome and return parsed result."""
    name = os.path.basename(queryfile)
    outfilename = 'blast/blastout_%s.xml' % name

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
