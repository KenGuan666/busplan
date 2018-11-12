'''
CS 170 Project Design Doc

Kenny Huang, Ruihan Guan, Yin Tang


Our team decided that *using greedy algorithm to add each person to the bus
that has the most friends* is likely a good approximation for the problem.


Our proposed algorithm will first look at the graph and each given constraints:

1. Set the weight of all edges to sum of number of incident edges of both end vertices,
and add an edge of weight 0 between any possible combination of two vertices,
if one doesn't exist.

2. For each rowdy group, discard it if its size is larger than bus capacity.
Otherwise, for every two vertices in the rowdy group, *decrease weight of edge
between them by some number* that is a positive function of number of friends and
inversely proportionate to the size of the rowdy group. For now, let the number be:
                f(x) = #sum of num of friends/(size of rowdy group - 1)^2


Then, calculate the sum of weight of all incident edges for each vertex and place
them in a max priority queue. Thus a higher position in the queue means more friends,
friends having more friends, less rowdy groups, and rowdy groups having less inpact.

Finally, for each bus, greedily add the node at the highest position, then the
neighbor with highest edge weight in between, then a neighbor of either node
with highest edge weight in between, ... until the bus is full, or the next edge
has non-positive value.


The proposed algorithm should work well in many cases because it exploits the
popularity of people and takes into account the "impact" of rowdy groups relative
to its size. But it likely fails on problems with small bus sizes where popularity
isn't a major concern, or when rowdy groups coincide with friend circles on a
large scale. In the future we may incorporate dynamic edge weights by adding
pointers from each edge to other edges that represent the same rowdy group.

'''
