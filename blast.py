"""A wrapper around the BLAST tool."""

import parse
import logging
import subprocess

logger = logging.getLogger('root')


def blast(seqid, query, dbpath, outfile):
    """Run a blast search, check outcome and return parsed result."""
    with open('blast/query.fas', 'w') as f:
        f.write('>%s\n%s' % (seqid, query))

    args = (
        'bin/blastn',
        '-query', 'blast/query.fas',
        '-db', dbpath,
        '-out', outfile,
        '-outfmt', '5',
        "-evalue", '1E-50',
        "-max_target_seqs", '10',
    )
    try:
        subprocess.run(args, capture_output=True, check=True)
    except subprocess.CalledProcessException as exc:
        logger.error(exc.stderr)
        raise exc

    return parse.blast_xml(outfile)
