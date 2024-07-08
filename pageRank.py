import numpy as np

def page_rank(graph, damping_factor=0.85, max_iterations=100, tol=1e-6):
    """
    Rangira povezane strane koriscenjem Page Rank algoritma

    Parametri:
    - graph: graf objekat koji koristi metode vertices() za pristup cvorovima i edges() za pristup granama
    - damping_factor: Vjerovatnoca pracenja veze (postavljena na 0.85).
    - max_iterations: Maksimalan broj iteracija
    - tol: tolerancija konvergencije

    Vraca:
    - Rjecnik koji sadrzi kljuc koji je naziv strane i vrijednost koja predstavlja rank
    """

    num_pages = len(graph.vertices())   #broj strana
    pagerank_scores = {page: 1 / num_pages for page in graph.vertices()}        #incijalizacija skora

    # ulazne i izlazne veze
    incoming_links = {page: [] for page in graph.vertices()}
    outgoing_links = {page: 0 for page in graph.vertices()}

    for from_vertex, to_vertex in graph.edges():
        incoming_links[to_vertex].append(from_vertex)
        outgoing_links[from_vertex] += 1

    for iteration in range(max_iterations):
        new_pagerank_scores = {}
        total_residual = 0

        
        for page in graph.vertices():
            incoming_contribution = sum(
                pagerank_scores[in_link] / outgoing_links[in_link]
                for in_link in incoming_links[page]
            )

            # apdejt skora
            new_pagerank_scores[page] = (1 - damping_factor) / num_pages + damping_factor * incoming_contribution

            total_residual += abs(new_pagerank_scores[page] - pagerank_scores[page])

        pagerank_scores = new_pagerank_scores

        # provjera konvergencije
        if total_residual < tol:
            break

    return pagerank_scores
