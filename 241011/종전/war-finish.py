# 입력 받기
n = int(input())  # 격자의 크기
grid = [list(map(int, input().split())) for _ in range(n)]  # 인구수를 입력 받음

# 방향 벡터 설정 (반시계 순회: 아래 → 왼쪽 → 위 → 오른쪽)
directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

# 최소 인구 수 차이를 구하기 위한 초기값 설정
min_population_diff = float('inf')

# 가능한 모든 x, y, d1, d2를 선택하여 최소 인구 수 차이를 구함
for x in range(n):
    for y in range(n):
        for d1 in range(1, n):
            for d2 in range(1, n):
                # 조건: (x + d1 + d2) < n  and (0 ≤ y - d1) and (y + d2) < n
                if x + d1 + d2 >= n or y - d1 < 0 or y + d2 >= n:
                    continue

                # 각 부족의 인구 수 초기화
                population = [0] * 5
                area = [[0] * n for _ in range(n)]  # 각 칸의 부족 정보를 저장

                # 1번 부족 경계선 설정 (기울어진 직사각형 경계 그리기)
                for i in range(d1 + 1):
                    area[x + i][y - i] = 5  # 1번 경계선
                    area[x + d2 + i][y + d2 - i] = 5  # 3번 경계선

                for i in range(d2 + 1):
                    area[x + i][y + i] = 5  # 2번 경계선
                    area[x + d1 + i][y - d1 + i] = 5  # 4번 경계선

                # 1번 부족 영역 채우기 (경계 내부 채우기)
                for i in range(x + 1, x + d1 + d2):
                    inside = False
                    for j in range(n):
                        if area[i][j] == 5:  # 경계를 만나면 inside 상태를 토글
                            inside = not inside
                        if inside:
                            area[i][j] = 5

                # 나머지 부족 영역 채우기
                for r in range(n):
                    for c in range(n):
                        if area[r][c] == 5:  # 1번 부족은 이미 채워졌으므로 패스
                            continue
                        # 각 위치별로 부족 번호를 지정
                        if 0 <= r < x + d1 and 0 <= c <= y:  # 2번 부족
                            area[r][c] = 1
                        elif 0 <= r <= x + d2 and y < c < n:  # 3번 부족
                            area[r][c] = 2
                        elif x + d1 <= r < n and 0 <= c < y - d1 + d2:  # 4번 부족
                            area[r][c] = 3
                        elif x + d2 < r < n and y - d1 + d2 <= c < n:  # 5번 부족
                            area[r][c] = 4

                # 각 부족의 인구 수 계산
                for i in range(n):
                    for j in range(n):
                        population[area[i][j] - 1] += grid[i][j]

                # 최대 인구와 최소 인구의 차이 계산
                max_population = max(population)
                min_population = min(population)
                min_population_diff = min(min_population_diff, max_population - min_population)

# 최소 인구 수 차이 출력
print(min_population_diff)