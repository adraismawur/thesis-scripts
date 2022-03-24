
def get_core_pfam(core_pfam_tsv):
    core_pfam_accessions = set()
    core_pfam_names = set()
    with open(core_pfam_tsv) as core_pfam_file:
        # skip line
        core_pfam_file.readline()
        # read accessions
        for line in core_pfam_file:
            lineparts = line.split("\t")
            accession = lineparts[0]
            name = lineparts[1]
            core_pfam_accessions.add(accession)
            core_pfam_names.add(name)
    return core_pfam_accessions, core_pfam_names

def get_bio_pfam(bio_pfam_tsv):
    bio_pfam_accessions = set()
    bio_pfam_names = set()
    with open(bio_pfam_tsv) as bio_pfam_file:
        # skip line
        bio_pfam_file.readline()
        # read accessions
        for line in bio_pfam_file:
            lineparts = line.split("\t")
            accession = lineparts[0]
            name = lineparts[1]
            bio_pfam_accessions.add(accession)
            bio_pfam_names.add(name)
    return bio_pfam_accessions, bio_pfam_names
