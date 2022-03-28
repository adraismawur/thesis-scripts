def get_bgc_ids(db):
    return [row["bgcid"] for row in db.select(
        "bgc",
        "",
        props=[
            "bgc.id as bgcid"
        ]
    )]

def get_hmm_ids(db):
    return [row["hmmid"] for row in db.select(
        "hmm",
        "",
        props=[
            "hmm.id as hmmid"
        ]
    )]

def get_bgc_id_name_dict(db):
    bgc_id_name_dict = dict()
    for row in db.select(
        "bgc",
        "",
        props=[
            "bgc.id",
            "bgc.name"
        ]
    ):
        bgc_id_name_dict[row["id"]] = row["name"].split('/')[1]
    return bgc_id_name_dict


def get_features(db):
    return db.select(
        "bgc,hmm,bgc_features",
        " WHERE bgc_features.bgc_id=bgc.id" +
        " AND bgc_features.hmm_id=hmm.id" +
        "",
        props=["bgc_features.bgc_id",
                "bgc_features.hmm_id",
                "bgc_features.value"],
        as_tuples=True
    )

def get_core_pfam_ids(db, core_pfam_accessions, core_pfam_names):
    query_results = db.select(
        "hmm",
        "",
        props=[
            "hmm.id",
            "hmm.accession",
            "hmm.name"
        ]
    )
    result = []
    for row in query_results:
        if row["accession"] in core_pfam_accessions or row["name"] in core_pfam_names:
            result.append(row["id"])
    return result

def get_bio_pfam_ids(db, bio_pfam_accessions, bio_pfam_names):
    query_results = db.select(
        "hmm",
        "",
        props=[
            "hmm.id",
            "hmm.accession",
            "hmm.name"
        ]
    )
    result = []
    for row in query_results:
        if row["accession"] in bio_pfam_accessions or row["name"] in bio_pfam_names:
            result.append(row["id"])
    return result
