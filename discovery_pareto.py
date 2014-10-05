import random 
# nothing to see here, move along.
#
# exploratory: I wanted to understand how different alpha values skewed the
#              pareto distribution without spending a lot of time on Wikipedia
# ultimately I decided I wanted a normal distribution with carefully chosen mu
# and sigma

num_alphas = 5
threshold = 2
counters = [[]] + [[]]*num_alphas
for alpha in range(1, num_alphas+1):
    for test in range(1000):
        counter = 1
        while random.paretovariate(alpha) < threshold:
            counter += 1
        counters[alpha].append(counter)

for alpha in range(1,num_alphas+1):
    counts = counters[alpha]
    print alpha, min(counts), sum(counts)/1000, max(counts)
