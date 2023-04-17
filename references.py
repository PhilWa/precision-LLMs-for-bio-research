from utils import (
    calc_embeddings,
    render_abstract_ranking,
    distance_between_vector_and_vectors,
    get_data,
)


def add_references(ans: str, top_n: int):
    """
    Add references to a given answer by finding the top_n most similar abstracts
    using their precomputed embeddings.
    """
    ans_embeddings = calc_embeddings(ans)
    abs_embeddings = get_data("abstract_embeddings")
    similarities = distance_between_vector_and_vectors(ans_embeddings, abs_embeddings)

    abstracts = get_data("abstracts")

    top_id = (-similarities).argsort()[:top_n]

    return render_abstract_ranking(abstracts, top_id)


def add_ref(ans: str, top_n: int):
    """
    Add references to a given answer by finding the top_n most similar
    microbiology preprints using their precomputed embeddings.
    """
    ans_embeddings = calc_embeddings(ans, "bert")
    abs_embeddings = get_data("bio_axv_embeddings_microbiology")
    similarities = distance_between_vector_and_vectors(ans_embeddings, abs_embeddings)
    abstracts = get_data("bio_axv_preprints_microbiology")
    top_id = (-similarities).argsort()[:top_n]
    return render_abstract_ranking(abstracts, top_id)


def identify_domain(sentence: str):
    # Match content from config_knowledgegraph to
    # 1. subset literature
    # 2. provide context information
    return None
