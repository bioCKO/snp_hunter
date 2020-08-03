"""A wrapper around the BLAST tool."""

import logging
import subprocess
from parse import BlastResult

logger = logging.getLogger('root')


def blast(seqid, query, dbpath):
    """Run a blast search, check outcome and return parsed result."""
    queryfile = 'blast/query_%s.fas' % seqid
    outfile = 'blast/blastout_%s.xml' % seqid
    with open(queryfile, 'w') as f:
        f.write('>%s\n%s' % (seqid, query))

    args = (
        'bin/blastn',
        '-db', dbpath,
        '-query', queryfile,
        '-out', outfile,
        '-outfmt', '5',
        "-evalue", '1E-50',
        "-max_target_seqs", '10',
    )
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stderr)
        raise exc

    return BlastResult(outfile)
