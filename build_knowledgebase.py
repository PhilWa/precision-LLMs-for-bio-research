from utils import build_knowledgebase

### Metabolites and proteins have the common key PathBank ID,
### In pathways the PathBank ID	is named SMPDB

# TODO integrate BioNumbers.xls

# Metabolite database
COL_NAMES = [
    "Metabolite_Name",
    "HMDB_ID",
    "KEGG_ID",
    "ChEBI_ID",
    "DrugBank_ID",
    "CAS",
    "Formula",
]
build_knowledgebase(
    dir="data/pathbank_all_metabolites.csv",
    db_name="collections.sqlite",
    table_name="pathbank_all_metabolites",
    column_names=COL_NAMES,
    set_pk="PathBank_ID",
)

# Protein database
COL_NAMES = [
    "Uniprot_ID",
    "Protein_Name",
    "HMDBP_ID",
    "DrugBank_ID",
    "GenBank_ID",
    "Gene_Name",
    "Locus",
]
build_knowledgebase(
    dir="data/pathbank_all_proteins.csv",
    db_name="collections.sqlite",
    table_name="pathbank_all_proteins",
    column_names=COL_NAMES,
    set_pk="PathBank_ID",
)

# Pathway database
COL_NAMES = [
    "pathway_name",
    "Description",
]
build_knowledgebase(
    dir="data/pathbank_pathways.csv",
    db_name="collections.sqlite",
    table_name="pathbank_pathways",
    column_names=COL_NAMES,
    set_pk="SMPDB_ID",
)
