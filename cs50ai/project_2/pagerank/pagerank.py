import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = dict()
    corpus_structure = corpus
    corpus_length = len(corpus_structure)
    for p in corpus_structure:
        distribution[p] = (1-damping_factor)/corpus_length
        if p in corpus_structure[page]:
            distribution[p] += damping_factor / len(corpus_structure[page]) 
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initial page selection
    page = random.choice([p for p in corpus])
    result = dict()
    for i in range(n):
        t = transition_model(corpus, page, damping_factor)
        population = [p for p in t]
        weights = [t[p] for p in t]
        page = random.choice(
            random.choices(population,weights,k=10000)
        )
        try:
            result[page] += 1
        except KeyError:
            result[page] = 1
    
    total = sum([result[i] for i in result])
    for i in result:
        result[i] = result[i]/total
    
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize variables
    c = corpus
    N = len(c)
    d = damping_factor
    # returns dict with the other page name and number of links, 
    # if the other page links to page p
    numlinks = lambda p, cp : {i:len(cp[i]) for i in cp if p in cp[i]}
    # Initialize ranks to be equal for all pages in corpus
    rank0 = {p:1/N for p in c}

    flag = True
    while flag:
        flag = False
        rank1 = dict()
        for p in rank0:
            pagelinks = numlinks(p=p,cp=corpus)
            rank1[p] = (1-d)/N + d*sum([rank0[i]/pagelinks[i] for i in pagelinks])
            if abs(rank1[p] - rank0[p]) > 0.001:
                flag = True
        rank0 = rank1

    return rank1


if __name__ == "__main__":
    main()
