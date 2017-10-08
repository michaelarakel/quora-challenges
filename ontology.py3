from collections import defaultdict


class TrieNode(object):
    __slots__ = ('count', 'children')

    def __init__(self):
        self.count = 0
        self.children = defaultdict(TrieNode)


class Trie(object):
    __slots__ = ('root', )

    def __init__(self):
        self.root = TrieNode()

    def insert(self, line):
        current_node = self.root
        for char in line:
            current_node.count += 1
            current_node = current_node.children[char]
        current_node.count += 1

    def get_count(self, line):
        current_node = self.root
        for char in line:
            if char not in current_node.children:
                return 0
            current_node = current_node.children[char]
        return current_node.count


class SegmentTreeOfTries(object):
    __slots__ = ('size', 'tree')

    def __init__(self, size):
        self.size = size
        self.tree = [Trie() for _ in range(4 * size)]

    def update(self, index, line):
        self._update(index, line, 1, 0, self.size)

    def _update(self, index, line, node_num, range_start, range_end):
        if range_start >= range_end:
            return

        self.tree[node_num].insert(line)

        if range_end - range_start == 1:
            return

        range_mid = (range_start + range_end) // 2
        if index < range_mid:
            self._update(
                index, line, node_num << 1, range_start, range_mid
            )
        else:
            self._update(
                index, line, (node_num << 1) + 1, range_mid, range_end
            )

    def query_prefix(self, query_range_start, query_range_end, prefix):
        return self._query_prefix(
            query_range_start, query_range_end, prefix,
            1, 0, self.size
        )

    def _query_prefix(self, query_range_start, query_range_end, prefix, node_num, range_start, range_end):
        if range_start >= range_end:
            return 0

        if query_range_start >= query_range_end:
            return 0

        if query_range_start == range_start and query_range_end == range_end:
            return self.tree[node_num].get_count(prefix)

        range_mid = (range_start + range_end) // 2

        if query_range_end <= range_mid:
            return self._query_prefix(
                query_range_start, query_range_end, prefix, node_num << 1, range_start, range_mid
            )
        elif query_range_start > range_mid:
            return self._query_prefix(
                query_range_start, query_range_end, prefix, (node_num << 1) + 1, range_mid, range_end
            )

        return self._query_prefix(
            query_range_start, range_mid, prefix, node_num << 1, range_start, range_mid
        ) + self._query_prefix(
            range_mid, query_range_end, prefix, (node_num << 1) + 1, range_mid, range_end
        )


def construct_topic_tree(line):
    lines = line.split(' ')
    stack = []
    current_head = None

    topic_range_start = {}
    topic_range_end = {}

    for topic in lines:
        if topic == ')':
            current_head = stack.pop()
            topic_range_end[current_head] = current_head_num
        elif topic == '(':
            stack.append(current_head)
            current_head = None
        else:
            current_head = topic
            current_head_num = len(topic_range_start)
            topic_range_start[current_head] = current_head_num
            topic_range_end[current_head] = current_head_num

            if stack:
                topic_range_end[stack[-1]] = current_head_num

    return topic_range_start, topic_range_end


def main():
    number_of_nodes = int(input())
    topic_range_start, topic_range_end = construct_topic_tree(input())
    segment_tree = SegmentTreeOfTries(number_of_nodes)

    updates = int(input())
    for _ in range(updates):
        topic, question = input().split(': ')
        segment_tree.update(
            topic_range_start[topic], question
        )

    queries = int(input())
    for _ in range(queries):
        topic, _, prefix = input().partition(' ')
        print(
            segment_tree.query_prefix(
                topic_range_start[topic], topic_range_end[topic] + 1, prefix
            )
        )

if __name__ == '__main__':
    main()
