#include <algorithm>
#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>

typedef std::vector< std::vector<int> > graph;

namespace std {
    template<>
    struct hash< std::pair<int, int> > {
        size_t operator () (const std::pair<int, int>& p) const {
            return ((size_t)p.first) ^ ((size_t)p.second);
        }
    };
}

struct MinExpectedTimeSolver {
    MinExpectedTimeSolver(const graph& g, const std::vector<int>& time): g(g), time(time) {}
    
    int solve() {
        double smallest = 1000 * 1000 * 1000;
        int best = -1;
        for (int node = 0; node < (int)g.size(); ++node) {
            double value = dynamic_programming(node);
            if (value < smallest) {
                smallest = value;
                best = node;
            }
        }
        
        return best;
    }
    
    double dynamic_programming(int node, int parent = -1) {
        std::pair<int, int> cache_key = {node, parent};
        
        auto it = dp_cache.find(cache_key);
        if (it != dp_cache.end()) {
            return it->second;
        }
        
        double expected_value = 0;
        int neighbours_to_visit = 0;
        
        for (auto neighbour: g[node]) {
            if (neighbour == parent) {
                continue;
            }
            ++neighbours_to_visit;
            expected_value += dynamic_programming(neighbour, node);
        }
        
        if (neighbours_to_visit != 0) {
            expected_value /= neighbours_to_visit;
        }
        expected_value += time[node];
        
        dp_cache.insert({cache_key, expected_value});
        return expected_value;
    }
    
    graph g;
    std::vector<int> time;
    std::unordered_map<std::pair<int, int>, double> dp_cache;
};

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int n;
    std::cin >> n;
    
    std::vector< std::vector<int> > g(n);
    for (int i = 0; i < n; ++i) {
        g[i].reserve(10);
    }
    
    std::vector<int> reading_times(n);

    for (auto& time: reading_times) {
        std::cin >> time;
    }

    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        std::cin >> u >> v;
        --u, --v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    auto solver = MinExpectedTimeSolver(g, reading_times);

    std::cout << solver.solve() + 1;
}
