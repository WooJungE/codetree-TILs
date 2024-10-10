# 입력 받기
n, m, t = map(int, input().split())  # n: 행의 수, m: 열의 수, t: 시간(초)

# 방의 상태 입력 받기
room = []
for _ in range(n):
    room.append(list(map(int, input().split())))

# 시공의 돌풍 위치 찾기 (1열에 -1이 위치한 두 칸의 행 번호를 찾음)
cleaner_top = -1  # 위쪽 시공의 돌풍 위치
cleaner_bottom = -1  # 아래쪽 시공의 돌풍 위치
for i in range(n):
    if room[i][0] == -1:
        if cleaner_top == -1:
            cleaner_top = i  # 위쪽 시공의 돌풍 위치 설정
        else:
            cleaner_bottom = i  # 아래쪽 시공의 돌풍 위치 설정
            break

# 상하좌우 방향 이동
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우

# 먼지 확산 함수
def spread_dust():
    # 확산 후의 방 상태를 저장할 임시 배열
    new_room = [[0] * m for _ in range(n)]
    # 시공의 돌풍 위치는 그대로 유지
    new_room[cleaner_top][0] = -1
    new_room[cleaner_bottom][0] = -1

    # 모든 칸에 대해서 확산을 진행
    for i in range(n):
        for j in range(m):
            if room[i][j] > 0:  # 먼지가 있는 경우
                spread_amount = room[i][j] // 5  # 확산될 양 (정수 나누기)
                if spread_amount > 0:
                    spread_count = 0  # 몇 개의 칸에 확산되었는지

                    # 4방향으로 확산 시도
                    for dr, dc in directions:
                        ni, nj = i + dr, j + dc
                        if 0 <= ni < n and 0 <= nj < m and room[ni][nj] != -1:
                            new_room[ni][nj] += spread_amount
                            spread_count += 1

                    # 원래 칸의 먼지 양은 확산된 양만큼 줄어듬
                    new_room[i][j] += room[i][j] - (spread_amount * spread_count)
                else:
                    new_room[i][j] += room[i][j]  # 확산되지 않으면 그대로 유지

    return new_room

# 공기 청정기의 바람 순환 함수
def operate_cleaner():
    # 위쪽 공기 청정기 (반시계 방향 순환)
    # 위 -> 좌 -> 하 -> 우 (반시계 방향)
    # 1열 왼쪽으로 당기기
    for i in range(cleaner_top - 1, 0, -1):
        room[i][0] = room[i - 1][0]
    # 1행 위쪽으로 당기기
    for j in range(m - 1):
        room[0][j] = room[0][j + 1]
    # m열 오른쪽으로 당기기
    for i in range(cleaner_top):
        room[i][m - 1] = room[i + 1][m - 1]
    # 공기청정기 아래쪽으로 당기기
    for j in range(m - 1, 1, -1):
        room[cleaner_top][j] = room[cleaner_top][j - 1]
    room[cleaner_top][1] = 0  # 공기청정기로 들어간 먼지는 사라짐

    # 아래쪽 공기 청정기 (시계 방향 순환)
    # 아래 -> 좌 -> 위 -> 우 (시계 방향)
    # 1열 왼쪽으로 당기기
    for i in range(cleaner_bottom + 1, n - 1):
        room[i][0] = room[i + 1][0]
    # n행 아래쪽으로 당기기
    for j in range(m - 1):
        room[n - 1][j] = room[n - 1][j + 1]
    # m열 오른쪽으로 당기기
    for i in range(n - 1, cleaner_bottom, -1):
        room[i][m - 1] = room[i - 1][m - 1]
    # 공기청정기 위쪽으로 당기기
    for j in range(m - 1, 1, -1):
        room[cleaner_bottom][j] = room[cleaner_bottom][j - 1]
    room[cleaner_bottom][1] = 0  # 공기청정기로 들어간 먼지는 사라짐

# t초 동안 시뮬레이션
for _ in range(t):
    room = spread_dust()  # 먼지 확산
    operate_cleaner()  # 공기 청정기 작동

# t초 후 방에 남아있는 먼지의 총합 계산
total_dust = 0
for i in range(n):
    for j in range(m):
        if room[i][j] > 0:  # 먼지가 있는 경우만
            total_dust += room[i][j]

print(total_dust)