"""Parse output files to Python objects."""

from bs4 import BeautifulSoup


class BlastResult:
    """Contains result data from a single BLAST search."""

    def __init__(self, xml_path):
        """Read in and parse XML output."""
        self.raw_xml = open(xml_path).read()
        self.soup = BeautifulSoup(self.raw_xml, 'xml')
        self.algorithm = self.get_alg()
        self.db = self.soup.find('BlastOutput_db').text
        self.query = self.soup.find('BlastOutput_query-def').text
        self.query_length = self.soup.find('BlastOutput_query-len').text
        self.hits = self.get_hits()

    def get_alg(self):
        """Parse out blast program used."""
        alg = self.soup.find('BlastOutput_program')
        return alg.text

    def get_hits(self):
        """Parse hit stats and return list of hits."""
        return [Hit(h) for h in self.soup.find_all('Hit')]

    def report(self):
        """Return string report of this hit."""
        lines = []
        lines.append("### Output from %s ###" % self.algorithm)
        lines.append("Query: %s (%s bp)" % (self.query, self.query_length))
        lines.append("DB:    %s" % self.db)
        lines.append("Hits:  %s" % len(self.hits))
        lines.append("")
        for i, hit in enumerate(self.hits):
            lines.append("Hit %s: %s (%s bp)" % (i + 1, hit.contig_id, hit.length))
            lines.append("%s HSPs" % len(hit.hsps))
            lines.append("")
            for k, hsp in enumerate(hit.hsps):
                lines.append("HSP %s" % (k + 1))
                lines.append((
                    ("Identity:   %.0f%%" % hsp.identity_pc).ljust(25)
                    + ("E-value:  %.2e" % hsp.evalue).ljust(25)
                    + ("Q-cover: %s%%" % hsp.query_cover)
                ))
                lines.append((
                    ("Identities: %s/%s" %
                        (hsp.identities, hsp.length)).ljust(25)
                    + ("Bitscore: %s" % hsp.bitscore).ljust(25)
                    + ("Q-range: %s:%s" %
                        (hsp.query_from, hsp.query_to))
                ))
                lines.append((
                    ("Frame:      %s" % hsp.hit_frame).ljust(25)
                    + ("Gaps:     %s" % hsp.gaps).ljust(25)
                    + ("S-range: %s:%s" %
                        (hsp.sub_from, hsp.sub_to))
                ))
                lines.append("")
                lines.append(str(hsp) + '\n\n')
        return '\n'.join(lines)


class Hit:
    """Holds alignment stats for a single BLAST hit."""

    def __init__(self, soup):
        """Parse hit stats from hit soup."""
        self.soup = soup
        self.contig_id = self.get_id()
        self.length = int(self.soup.find('Hit_len').text)
        self.hsps = self.get_hsps()

    def get_id(self):
        """Return the hit subject contig ID."""
        hit_id = self.soup.find('Hit_id').text
        accession = self.soup.find('Hit_accession').text
        return [
            x for x in (hit_id, accession)
            if 'no definition' not in x.lower()
        ][-1]

    def get_hsps(self):
        """Return a list of high-scoring pairs for this hit."""
        return [Hsp(hsp, self) for hsp in self.soup.find_all('Hsp')]


class Hsp:
    """Holds alignment stats for a single high-scoring pair."""

    def __init__(self, soup, hit):
        """Read in HSP XML soup and parse out hit stats."""
        self.soup = soup
        self.parent = hit
        self.bitscore = float(self.soup.find('Hsp_bit-score').text)
        self.evalue = float(self.soup.find('Hsp_evalue').text)
        self.query_from = int(self.soup.find('Hsp_query-from').text)
        self.query_to = int(self.soup.find('Hsp_query-to').text)
        self.sub_from = int(self.soup.find('Hsp_hit-from').text)
        self.sub_to = int(self.soup.find('Hsp_hit-to').text)
        self.hit_frame = int(self.soup.find('Hsp_hit-frame').text)
        self.identities = int(self.soup.find('Hsp_identity').text)
        self.positives = int(self.soup.find('Hsp_positive').text)
        self.gaps = int(self.soup.find('Hsp_gaps').text)
        self.align_len = int(self.soup.find('Hsp_align-len').text)
        self.align_query = self.soup.find('Hsp_qseq').text
        self.align_subject = self.soup.find('Hsp_hseq').text
        self.align_midline = self.soup.find('Hsp_midline').text
        self.length = self.query_to - self.query_from
        self.identity_pc = self.get_identity()
        self.query_cover = self.get_query_coverage()

    def __str__(self):
        """Return alignment as printable string."""
        def wrap_lines(string, n=80):
            """Wrap a string at n characters and return as list."""
            lines = []
            while len(string) > n:
                lines.append(string[:n])
                string = string[n:]
            lines.append(string)
            return lines

        def scale_generator(n=80):
            """Generate text scale bar in lines of length n."""
            x = -1 * n
            while True:
                x += n
                yield (''.join([
                        str(x + i).ljust(10) for i in range(0, int(n), 10)
                    ])
                    + '\n' + ''.join([
                        '|....:....' for i in range(0, int(n), 10)
                    ])
                )

        i = 0
        lines = []
        query = wrap_lines(self.align_query)
        midline = wrap_lines(self.align_midline)
        subject = wrap_lines(self.align_subject)
        for scale in scale_generator():
            try:
                lines.append('\n'.join([
                    scale,
                    query[i],
                    midline[i],
                    subject[i],
                ]))
                i += 1
            except IndexError:
                break
        return '\n\n'.join(lines)

    def get_identity(self):
        """Return percent identity with query sequence."""
        return 100 * self.identities / (
            self.query_to - self.query_from
        )

    def get_query_coverage(self):
        """Return percentage coverage of query sequence by this hsp."""
        return 100 * (self.query_to - self.query_from) / self.parent.length


if __name__ == '__main__':
    path = 'blast/test_blastout.xml'
    raw_xml = open(path).read()
    soup = BeautifulSoup(raw_xml, 'xml')
    x = soup.find('Hsp_align-len')

    # result = BlastResult(path)
    # print(result.report())
