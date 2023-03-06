//  g++ -std=c++11 unordered_map_and_vector_demo.cpp
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

int main() {
    //std::unordered_multimap<std::string, std::string> segments;
    // auto range = segments.equal_range("hello");

    std::unordered_multimap<int,char> map = {{1,'a'},{1,'b'},{1,'d'},{2,'b'}};
    auto range = map.equal_range(8);
  
    for (auto it = range.first; it != range.second; ++it) {
        std::cout << "item:" << it->first << ' ' << it->second << '\n';
    }
  
    // demo of segmentation fault for push back null to a vector:
    std::vector<std::string> list; 
    std::vector<std::string> emptyList;
    list.push_back(nullptr);
    list.insert(list.end(), emptyList.begin(), emptyList.end());

	return 0;
}
