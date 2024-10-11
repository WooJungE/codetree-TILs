from collections import defaultdict

# 입력 받기
n, m, k = map(int, input().split())  # n: 행의 수, m: 열의 수, k: 곰팡이 수

# 곰팡이 정보 저장
molds = {}  # (x, y) -> (speed, direction, size)

for _ in range(k):
    x, y, s, d, b = map(int, input().split())
    molds[(x - 1, y - 1)] = (s, d, b)  # 좌표를 0-based로 저장 (속도, 방향, 크기)

# 방향 설정 (위, 아래, 오른쪽, 왼쪽)
directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # (위, 아래, 오른쪽, 왼쪽)

# 인턴이 채취한 곰팡이 크기의 총합
total_mold_size = 0

# 인턴이 1열부터 m열까지 탐색
for col in range(m):
    # 1. 인턴이 현재 열에서 곰팡이 채취
    for row in range(n):
        if (row, col) in molds:  # 현재 위치에 곰팡이가 있으면
            total_mold_size += molds[(row, col)][2]  # 곰팡이의 크기를 더하고
            del molds[(row, col)]  # 해당 곰팡이를 채취했으므로 제거
            break  # 곰팡이를 한 마리만 채취하고 종료

    # 2. 곰팡이 이동
    new_molds = defaultdict(lambda: (0, 0, 0))  # 새로운 곰팡이 위치 저장 (속도, 방향, 크기)
    for (x, y), (speed, direction, size) in molds.items():
        # 곰팡이의 현재 방향과 속도를 계산하여 이동
        dx, dy = directions[direction - 1]  # 방향에 따른 이동 변화량
        
        # 이동할 거리를 계산 (벽을 반복해서 넘는 경우를 최적화)
        if direction in [1, 2]:  # 위쪽이나 아래쪽으로 이동하는 경우
            move_distance = speed % (2 * n - 2)  # 위아래 반복 경로를 고려
        else:  # 왼쪽이나 오른쪽으로 이동하는 경우
            move_distance = speed % (2 * m - 2)  # 좌우 반복 경로를 고려

        # 곰팡이 이동 (속도 move_distance만큼 이동)
        nx, ny = x, y
        for _ in range(move_distance):
            # 다음 위치로 이동
            nx += dx
            ny += dy

            # 벽에 부딪히면 방향 반대
            if nx < 0 or nx >= n:  # 행 벽에 부딪힌 경우
                direction = 2 if direction == 1 else 1  # 위 <-> 아래 방향 전환
                dx, dy = directions[direction - 1]
                nx += 2 * dx  # 방향 바꾼 후 원래 위치로 되돌리기
            if ny < 0 or ny >= m:  # 열 벽에 부딪힌 경우
                direction = 4 if direction == 3 else 3  # 왼쪽 <-> 오른쪽 방향 전환
                dx, dy = directions[direction - 1]
                ny += 2 * dy  # 방향 바꾼 후 원래 위치로 되돌리기

        # 이동 후 위치에 곰팡이 저장 (기존 곰팡이와 겹치면 큰 곰팡이가 남음)
        cur_speed, cur_direction, cur_size = new_molds[(nx, ny)]
        if cur_size < size:  # 기존 곰팡이보다 크기가 크면 덮어씀
            new_molds[(nx, ny)] = (speed, direction, size)

    # 3. 새로운 곰팡이 상태로 업데이트
    molds = new_molds

# 결과 출력 (채취한 곰팡이의 크기 총합)
print(total_mold_size)