# 입력 받기
N, M = map(int, input().split())
city_map = [list(map(int, input().split())) for _ in range(N)]

# 병원의 위치를 저장할 리스트
hospital_positions = []
total_empty_spaces = 0  # 전체 바이러스가 존재하는 공간의 개수 (벽을 제외한 공간)

# 병원의 위치와 전체 빈 공간 개수 파악
for i in range(N):
    for j in range(N):
        if city_map[i][j] == 2:  # 병원 위치
            hospital_positions.append((i, j))
        elif city_map[i][j] == 0:  # 바이러스가 있는 위치 (벽 제외)
            total_empty_spaces += 1

# 방향 벡터 (상, 하, 좌, 우)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# BFS를 통해 백신이 퍼지는 시간을 계산하는 함수 (리스트를 사용하여 큐 구현)
def bfs(hospitals):
    queue = []  # 리스트를 큐로 사용
    visited = [[-1] * N for _ in range(N)]  # 방문 배열 및 백신 전파 시간 초기화

    # 병원 위치들을 큐에 삽입하고 방문 처리
    for x, y in hospitals:
        queue.append((x, y))  # 큐에 병원 위치 삽입
        visited[x][y] = 0  # 병원 위치 방문 처리 및 시작 시간 0

    max_time = 0  # 바이러스 제거에 걸린 최대 시간
    empty_count = total_empty_spaces  # 제거해야 할 빈 공간의 개수

    while queue:
        x, y = queue.pop(0)  # 리스트의 첫 번째 요소를 꺼내어 처리 (큐에서 dequeue)

        # 상하좌우로 백신 확산
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # 다음 위치가 격자판 범위 내에 있고, 방문하지 않았으며, 벽이 아닌 경우
            if 0 <= nx < N and 0 <= ny < N and visited[nx][ny] == -1 and city_map[nx][ny] != 1:
                visited[nx][ny] = visited[x][y] + 1  # 전파 시간 증가
                queue.append((nx, ny))  # 다음 위치 큐에 추가
                if city_map[nx][ny] == 0:  # 바이러스가 있는 빈 공간일 경우
                    empty_count -= 1  # 바이러스 제거된 공간 개수 감소
                    max_time = visited[nx][ny]  # 전파 시간 갱신

    # 빈 공간이 남아 있으면 전부 제거하지 못한 경우 -1 반환
    if empty_count > 0:
        return float('inf')  # 불가능한 경우

    return max_time  # 모든 바이러스를 제거하는 데 걸린 시간 반환

# M개의 병원을 선택하는 조합을 직접 구현 (재귀함수 사용)
def generate_combinations(arr, comb, start, M, combinations_list):
    if len(comb) == M:
        combinations_list.append(comb[:])  # 현재 조합을 복사하여 저장
        return
    for i in range(start, len(arr)):
        comb.append(arr[i])  # 병원 위치 추가
        generate_combinations(arr, comb, i + 1, M, combinations_list)  # 다음 위치 선택
        comb.pop()  # 추가했던 병원 위치 제거 (백트래킹)

# 병원 위치 조합 리스트를 저장할 리스트
combinations_list = []
generate_combinations(hospital_positions, [], 0, M, combinations_list)  # 병원 위치 조합 생성

# 병원 위치 조합 중 최소 시간을 찾기
min_time = float('inf')

# 생성된 각 병원 조합에 대해 BFS를 수행하여 최소 시간을 계산
for hospitals in combinations_list:
    result_time = bfs(hospitals)
    min_time = min(min_time, result_time)

# 최소 시간 출력, 모든 바이러스 제거 불가능하면 -1 출력
print(min_time if min_time != float('inf') else -1)