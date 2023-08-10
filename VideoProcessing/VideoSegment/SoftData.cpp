#include <bits/stdc++.h>

const int N = 10000;
const int M = 10;

bool data[N][4][M];
int n;

std::pair<int, int> ans[9][4];

// std::pair<int, int> PairType(-1, -1);

std::pair<int, int> getFlash(int index, int line) {
	int Pos1 = 0, Pos2 = 0;
	int LastPos = -1, FirstPos = -1;

	for (int i = 1; i <= n; i++) {
		if (data[i][index][line]) LastPos = i;
		if (!data[i][index][line] && FirstPos == -1) FirstPos = i;

		// 判断闪烁是否结束
		if (i - LastPos >= 200) {
			return std::make_pair(FirstPos, LastPos);
		}
	}

	if (FirstPos == -1) LastPos = -1;
	if (LastPos == -1) FirstPos = -1;

	return std::make_pair(FirstPos, LastPos);
}

int main() {
	freopen("./output/P1.txt", "r", stdin);
	std::ifstream P2("../output/P2.txt");
	std::string line;

	// 输入
	scanf("%d", &n);

	for (int i = 1; i <= n; i++) {
		for (int k = 0; k <= 1; k++) {
			for (int j = 1; j <= 8; j++) {
				int t;
				scanf("%d", &t);
				data[i][k][j] = t;
			}
		}
	}
	printf("Read Data - Finished\n");

	// 去噪
	for (int i = 2; i < n; i++) {
		for (int j = 0; j <= 1; j++)
			for (int k = 1; k <= 8; k++)
				if (data[i][j][k] != data[i - 1][j][k] && data[i][j][k] != data[i + 1][j][k]) {
					data[i][j][k] = data[i - 1][j][k];
				}
	}

	printf("Denoising - Finished\n");

	printf("%d\n", n);

	for (int i = 0; i <= 1; i++)
		for (int j = 1; j <= 8; j++) {
			std::pair<int, int> PosInfo = getFlash(i, j);
			ans[j][i] = PosInfo;
			printf("%d %d %d %d\n", i, j, PosInfo.first, PosInfo.second);
		}

	freopen("./output/P2.txt", "w", stdout);

	printf("%d\n", n);
	
	for (int i = 0; i <= 1; i++)
		for (int j = 1; j <= 8; j++) {
			printf("%d %d %d %d\n", i, j, ans[j][i].first, ans[j][i].second);
		}

	return 0;
}