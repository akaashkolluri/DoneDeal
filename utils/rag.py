def get_relevant_doc():
    vo = voyageai.Client(api_key="pa--pNF1UDUmvupHNFQ1wxpHSUQ7aoNYO6xLg4-7E2fnEQ")

    # Convert contract description to embeddings
    description_embedding = vo.embed(description, model="voyage-law-2", input_type="query")
    print('part 1')
    # Search for relevant documents using Google Scholar

    params = {
    "api_key": "1ee8b33956fc55c31400c1bea5acb92349856a42c42362d8d0c06499a74f7c45",
    "engine": "google",
    "q": description,
    "google_domain": "scholar.google.com",
    "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    print('part 2')
    # Get embeddings for search results
    result_embeddings = []
    for result in results:  # Limit to top 10 results for efficiency
        # abstract = result.bib.get('abstract', '')
        # content = f"{title}\n{abstract}"
        embedding = vo.embed(result, model="voyage-law-2", input_type="document")
        result_embeddings.append((result, embedding))
    print('part 3')

    # Calculate cosine similarity between query and results
    def cosine_similarity(a, b):
        return (np.linalg.norm(np.array(a)) * np.linalg.norm(np.array(b)))

    similarities = [cosine_similarity(description_embedding, emb) for _, emb in result_embeddings]

    # Get the most relevant document
    most_relevant_index = np.argmax(similarities)
    most_relevant_doc = result_embeddings[most_relevant_index][0]
    
    return most_relevant_doc