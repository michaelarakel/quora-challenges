import sys
from collections import defaultdict


def dynamic_programming(node, parent, graph, times, cache):
	cache_key = (node, parent)

	if cache_key in cache:
		return cache[cache_key]

	expected_value = times[node]

	neighbours_to_visit = graph[node] - {parent}
	degree = len(neighbours_to_visit)
	expected_value += (
		0 if degree == 0 else
		sum(
			dynamic_programming(neighbour, node, graph, times, cache)
			for neighbour in neighbours_to_visit) / degree
	)

	cache[cache_key] = expected_value
	return expected_value


def get_expected_values_of_all_nodes(graph, times):
	cache = {}

	return [
		dynamic_programming(node, None, graph, times, cache)
		for node in range(len(graph))
	]


def main():
	nodes = int(input())
	times = list(map(int, input().split()))

	graph = defaultdict(set)
	for i in range(nodes - 1):
		u, v = map(int, input().split())
		u -= 1
		v -= 1
		graph[u].add(v)
		graph[v].add(u)

	expected_values = get_expected_values_of_all_nodes(
		graph, times
	)

	best_node = min(range(nodes), key=lambda x: expected_values[x])

	print(best_node + 1)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    main()
