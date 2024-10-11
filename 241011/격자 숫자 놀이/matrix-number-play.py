# 입력 받기
r, c, k = map(int, input().split())
r, c = r - 1, c - 1  # 1-based index를 0-based index로 변경

# 초기 격자판 설정 (3x3 행렬)
A = [list(map(int, input().split())) for _ in range(3)]

# 최대 행과 열 크기
MAX_SIZE = 100

# 행 정렬 수행 함수
def row_sort(matrix):
    max_col_size = 0
    new_matrix = []

    for row in matrix:
        # 1. 각 숫자의 빈도를 직접 계산
        frequency = {}
        for num in row:
            if num == 0:
                continue  # 0은 무시
            if num in frequency:
                frequency[num] += 1
            else:
                frequency[num] = 1

        # 2. 빈도 정보를 (숫자, 빈도) 형태로 리스트에 저장
        frequency_list = []
        for num, freq in frequency.items():
            frequency_list.append((num, freq))

        # 3. 출현 빈도 수가 적은 순으로, 출현 빈도가 같으면 숫자 크기 순으로 정렬
        frequency_list.sort(key=lambda x: (x[1], x[0]))

        # 4. 정렬된 결과를 [숫자, 빈도, 숫자, 빈도, ...] 형태로 변환
        new_row = []
        for num, freq in frequency_list:
            new_row.append(num)
            new_row.append(freq)

        # 5. 최대 열 크기 갱신
        max_col_size = max(max_col_size, len(new_row))

        # 6. 정렬된 행을 새로운 행렬에 추가
        new_matrix.append(new_row)

    # 7. 새로운 행렬의 모든 행의 길이를 max_col_size에 맞춰 0으로 채워줌
    for row in new_matrix:
        while len(row) < max_col_size:
            row.append(0)

    # 8. 길이가 100을 넘으면 100까지만 유지
    for i in range(len(new_matrix)):
        if len(new_matrix[i]) > MAX_SIZE:
            new_matrix[i] = new_matrix[i][:MAX_SIZE]

    return new_matrix

# 열 정렬 수행 함수
def col_sort(matrix):
    # 행과 열을 전환하여 열을 행처럼 처리
    transposed_matrix = list(zip(*matrix))  # 행과 열을 전환
    sorted_transposed_matrix = row_sort(transposed_matrix)
    sorted_matrix = list(zip(*sorted_transposed_matrix))  # 다시 행과 열을 원래대로 전환

    # 행 크기가 100을 넘으면 100까지만 유지
    if len(sorted_matrix) > MAX_SIZE:
        sorted_matrix = sorted_matrix[:MAX_SIZE]

    # 튜플 형태의 행렬을 리스트 형태로 변환
    return [list(row) for row in sorted_matrix]

# 연산 수행
time = 0
while time <= 100:
    # 목표 위치의 값이 k와 같으면 시간 출력 후 종료
    if r < len(A) and c < len(A[0]) and A[r][c] == k:
        print(time)
        break

    # 행의 개수 >= 열의 개수이면 행 정렬 수행
    if len(A) >= len(A[0]):
        A = row_sort(A)
    else:  # 행의 개수 < 열의 개수이면 열 정렬 수행
        A = col_sort(A)

    # 시간 증가
    time += 1
else:
    # 100초가 넘어도 목표 값에 도달하지 못하면 -1 출력
    print(-1)