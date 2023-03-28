from utils import (calc_embeddings,
                   render_abstract_ranking,
                   distance_between_vector_and_vectors,
                   get_data,)

def add_references(ans:str, top_n:int):

    ans_embeddings = calc_embeddings(ans)
    abs_embeddings = get_data('abstract_embeddings')
    similarities = distance_between_vector_and_vectors(ans_embeddings, abs_embeddings)

    abstracts = get_data('abstracts')

    top_id = (-similarities).argsort()[:top_n]

    return render_abstract_ranking(abstracts, top_id)


def add_ref(ans: str, top_n:int):
    ans_embeddings = calc_embeddings(ans, 'bert')
    abs_embeddings = get_data('bio_axv_embeddings_microbiology')
    similarities = distance_between_vector_and_vectors(ans_embeddings, abs_embeddings)
    abstracts = get_data('bio_axv_preprints_microbiology')
    top_id = (-similarities).argsort()[:top_n]
    return render_abstract_ranking(abstracts, top_id)
