#include <bits/stdc++.h>

using namespace std;

typedef int64_t i64;

template <typename T>
string vectostr(const vector<T>& vec) {
    stringstream s;
    s << "[ ";
    for (auto i : vec)
        s << i << ' ';
    s << ']';
    return s.str();
}

vector<vector<i64>> sumfibarr(vector<vector<i64>> s, i64 it) {
    int k = s.size();
    s.resize(it + 1);

    for (int i = k; i <= it; i++) {
        vector<i64> n(s[0].size(), 0);
        for (int j = i - k; j < i; j++) {
            transform(n.begin(), n.end(), s[j].begin(), n.begin(), plus());
        }
        s[i] = n;
    }

    return s;
}

vector<vector<i64>> create_ones_array(int i) {
    vector<vector<i64>> arr;
    for (int j = 0; j < i; j++) {
        vector<i64> a(i, 0);
        a[j] = 1;
        arr.push_back(a);
    }
    return arr;
}

int main() {
    vector<vector<double>> ratios;
    for (int i = 2; i <= 30; i++) {
        auto arr = create_ones_array(i);

        auto sum = sumfibarr(arr, 40 + i);
        vector<double> arr2(i);
        for (int j = 0; j < i; j++) {
            arr2[j] = ((double)sum.back()[j]) / (*(sum.end() - 2))[j];
        }
        ratios.push_back(arr2);
    }

    for (auto i : ratios) {
        cout << vectostr(i) << '\n';
    }

    cout << "ass\n";

    auto sum = sumfibarr(create_ones_array(10), 50);
    for (auto i : sum) {
        cout << vectostr(i) << '\n';
    }

    return 0;
}
