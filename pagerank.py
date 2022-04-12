
from mrjob.job import MRJob
# Want to implement a version of pagerank based on 
# the expression from here: https://www.geeksforgeeks.org/page-rank-algorithm-implementation/
# PR(u) = Sum of v belonging to Bu: PR(v)/L(v)
# v = a page
# u = a page
# Bu = the set containing all pages linking to page u
# L = Only unique links from a page that are not links to itself are valid as L

# The above PR will be combined with a rank of how profane a page is
# If the page is very profane it gets a lower rank
# If there are no profane words it gets no penalty



class MRPageRank(MRJob):

    def mapper(self, _, record):
        yield record, 1

    # Assume data used in G is already preprocessed and in a correct format  
    # Get input graph to look like this:
    # graph = { 
    #    "a" : ["b","c"],
    #    "b" : ["a", "d"],
    #    "c" : ["a", "d"],
    #    "d" : ["e"],
    #    "e" : ["d"]
    # }
    def pagerank(G, alpha=0.85, max_iter=100, tol=1.0e-6):
        if len(G) == 0:
            return {}
        
        for _ in range(max_iter):
            

            return None

if __name__ == '__main__':
    MRPageRank.run()
