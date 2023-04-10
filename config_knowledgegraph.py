# The idea is: We look for keyword in sentence.
# If there is a match then flag the key and the nested key
# The two keys can then have multiple usecases:
# 1. Inform context info
# 2. Dynamically subset knowledge graph
# 3. Further increase knowledge

common_cancer_cell_lines = [
    "HeLa",
    "MCF-7",
    "A549",
    "PC-3",
    "HCT116",
    "HT-29",
    "U-87 MG",
    "SK-OV-3",
    "K-562",
    "Jurkat",
    "DU-145",
    "A2780",
    "HepG2",
    "LNCaP",
    "SH-SY5Y",
]

common_ecoli_strains = [
    "K-12",
    "MG1655",
    "DH5α",
    "DH10B",
    "BL21",
    "BL21(DE3)",
    "JM109",
    "XL1-Blue",
    "JM110",
    "C600",
    "HB101",
    "TOP10",
    "W3110",
    "CGSC 5073",
]

model_organisms = {
    "bacteria": {
        "Escherichia coli": [
            "Escherichia coli",
            "E. coli",
            "coli",
            "Escherichia",
        ]
        + common_ecoli_strains,
        "Pseudomonas aeruginosa": [
            "Pseudomonas aeruginosa",
            "P. aeruginosa",
            "Pseudomonas",
        ],
        "Mycobacterium tuberculosis": [
            "Mycobacterium tuberculosis",
            "M. tuberculosis",
            "Mtb",
            "TB",
        ],
    },
    "mammals": {
        "Homo sapiens": [
            "Homo sapiens",
            "human",
            "H. sapiens",
        ]
        + common_cancer_cell_lines,
        "Mus musculus": [
            "Mus musculus",
            "mouse",
            "house mouse",
            "M. musculus",
        ],
        "Rattus norvegicus": [
            "Rattus norvegicus",
            "rat",
            "Norway rat",
            "brown rat",
            "R. norvegicus",
        ],
        "Bos taurus": [
            "Bos taurus",
            "cattle",
            "cow",
            "domestic cattle",
            "domestic cow",
            "B. taurus",
        ],
        "Macaca mulatta": [
            "Macaca mulatta",
            "rhesus macaque",
            "rhesus monkey",
            "M. mulatta",
        ],
    },
    "plants": {
        "Arabidopsis thaliana": [
            "Arabidopsis thaliana",
            "thale cress",
            "mouse-ear cress",
            "Arabidopsis",
            "A. thaliana",
        ],
        "Oryza sativa": [
            "Oryza sativa",
            "rice",
            "Asian rice",
            "O. sativa",
        ],
    },
    "nematodes": {
        "Caenorhabditis elegans": [
            "Caenorhabditis elegans",
            "C. elegans",
            "nematode",
            "roundworm",
            "Caenorhabditis",
        ],
        "Caenorhabditis briggsae": [
            "Caenorhabditis briggsae",
            "C. briggsae",
            "Caenorhabditis briggsae",
        ],
    },
    "insects": {
        "Drosophila melanogaster": [
            "Drosophila melanogaster",
            "fruit fly",
            "common fruit fly",
            "vinegar fly",
            "D. melanogaster",
        ],
        "Apis mellifera": [
            "Apis mellifera",
            "honey bee",
            "European honey bee",
            "A. mellifera",
        ],
    },
    "fungi": {
        "Saccharomyces cerevisiae": [
            "Saccharomyces cerevisiae",
            "baker's yeast",
            "brewer's yeast",
            "S. cerevisiae",
            "yeast",
            "Saccharomyces",
        ],
        "Schizosaccharomyces pombe": [
            "Schizosaccharomyces pombe",
            "fission yeast",
            "S. pombe",
            "Schizosaccharomyces",
        ],
    },
}
