from collections import deque


def number_of_ranges(upvotes, k, cmp):
	ranges_lengths = deque()

	current_length = 1
	for i in range(1, k):
		if cmp(upvotes[i], upvotes[i - 1]):
			current_length += 1
		else:
			ranges_lengths.append(current_length)
			current_length = 1

	ranges_lengths.append(current_length)

	current_number_of_ranges = sum(i * (i - 1) // 2 for i in ranges_lengths)

	results = [
		current_number_of_ranges
	]

	for i in range(k, len(upvotes)):
		current_number_of_ranges -= (
			ranges_lengths[0] * (ranges_lengths[0] - 1) // 2
		)
		ranges_lengths[0] -= 1
		current_number_of_ranges += (
			ranges_lengths[0] * (ranges_lengths[0] - 1) // 2
		)

		if cmp(upvotes[i], upvotes[i - 1]):
			last = ranges_lengths.pop()
			current_number_of_ranges -= (
				last * (last - 1) // 2
			)
			last += 1
			current_number_of_ranges += (
				last * (last - 1) // 2
			)
			ranges_lengths.append(last)
		else:
			ranges_lengths.append(1)

		if ranges_lengths[0] == 0:
			ranges_lengths.popleft()

		results.append(
			current_number_of_ranges
		)

	return results


def main():
	n, k = map(int, input().split())
	upvotes = list(
	    map(int, input().split())
	)

	non_decreasing_ranges = number_of_ranges(
		upvotes, k, cmp=lambda x, y: x >= y
	)
	non_increasing_ranges = number_of_ranges(
		upvotes, k, cmp=lambda x, y: x <= y
	)

	results = [
		non_dec - non_inc
		for non_dec, non_inc in zip(non_decreasing_ranges, non_increasing_ranges)
	]

	print(*results, sep='\n')


if __name__ == '__main__':
	main()
