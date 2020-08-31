# snp_hunter
Search transcriptome assemblies for sex-specific genes.

By using BLASTP to match male to female sequences (and vice versa), it should be possible to zero-in on sexually dimorphic transcripts which could be used as sex markers.

Specifically, we are looking for a matching transcript fromn the opposite sex which gives the impression of XY or WZ alleles.

These might have a higher identity at the protein level than the nucleotide level (assuming that protein function is conserved).

They might also have a closely matching ortholog in the other sex which contains SNPs (indicating that it is not an mRNA variant, but in fact a different gene).

These criteria are fulfilled by this small package, which runs BLASTP between a male and female set of transcripts and then filters the resulting matches.

Run SNP Hunter
-----

- Drop assembly FASTA files into `data/` (these may be full assembly or predicted coding-DNA/protein sequences)
- Run `build_blastdbs` to generate blast databases for the FASTA files you just dropped
- Modify the first lines of `hunter` to set query/db combinations that make sense
- Run `hunter`
- Check `output/` dir for result
