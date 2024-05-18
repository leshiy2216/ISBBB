#include <iostream>
#include <random>
#include <bitset>

void generate_single_binary_sequence() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<uint64_t> dis;

    uint64_t part1 = dis(gen);
    uint64_t part2 = dis(gen);

    std::bitset<64> bits1(part1);
    std::bitset<64> bits2(part2);

    std::cout << bits1.to_string() << bits2.to_string() << std::endl;
}

int main() {
    generate_single_binary_sequence();
    return 0;
}