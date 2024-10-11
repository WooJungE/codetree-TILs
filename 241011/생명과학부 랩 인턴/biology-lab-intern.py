# 입력 받기
n, m, k = map(int, input().split())  # n: 행의 수, m: 열의 수, k: 곰팡이 수

# 곰팡이 정보 초기화 (곰팡이의 위치를 저장할 리스트)
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
    new_positions = {}  # 새로운 곰팡이 위치 저장

    for (x, y), (speed, direction, size) in molds.items():
        # 이동 방향에 따른 변화량
        dx, dy = directions[direction - 1]
        
        # 벽을 넘어 반복되는 경우 최적화: (위아래 반복, 좌우 반복)
        if direction in [1, 2]:  # 위쪽이나 아래쪽으로 이동하는 경우
            effective_speed = speed % ((n - 1) * 2)  # 경로가 2 * (n - 1) 크기로 반복됨
        else:  # 왼쪽이나 오른쪽으로 이동하는 경우
            effective_speed = speed % ((m - 1) * 2)  # 경로가 2 * (m - 1) 크기로 반복됨

        # 이동 횟수만큼 반복하여 최종 위치 계산
        nx, ny = x, y
        for _ in range(effective_speed):
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

        # 새로운 위치에 곰팡이 저장
        if (nx, ny) not in new_positions:  # 새로운 위치에 곰팡이가 없으면 저장
            new_positions[(nx, ny)] = (speed, direction, size)
        else:  # 이미 곰팡이가 있다면 크기 비교
            existing_speed, existing_direction, existing_size = new_positions[(nx, ny)]
            if existing_size < size:  # 기존 곰팡이보다 크기가 큰 경우만 업데이트
                new_positions[(nx, ny)] = (speed, direction, size)

    # 3. 새로운 곰팡이 상태로 업데이트
    molds = new_positions

# 결과 출력 (채취한 곰팡이의 크기 총합)
print(total_mold_size)