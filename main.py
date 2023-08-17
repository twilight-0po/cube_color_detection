import cv2
import numpy as np
# 카메라 연결
cap = cv2.VideoCapture(0)

# 초기 사각형 크기 및 위치 설정
initial_size = 200
square_size = initial_size
square_center = (0, 0)

cube_color_list = [0, 0, 0, 0, 0, 0,]
got_color = False
cube_color = [], [], []
color_name = []
color_dict = {}
color_idx = 0
weight = 5  # rgb 차이 역치

cube_aspect = 1

def get_cube_color(color_idx, color_name, color_dict):

    cube_color = [], [], []

    for i in range(1, 4):
        for j in range(1, 4):
            center_x = top_left[0] + i * cell_size - cell_size // 2
            center_y = top_left[1] + j * cell_size - cell_size // 2

            # 중심 픽셀 RGB 값을 가져옴
            center_pixel = frame[center_y, center_x]
            center_rgb = list(center_pixel)
            if len(color_name) != 0:
                for color in color_name:
                    std_color = np.array(color_dict[str(color)])
                    rgb_diff = center_rgb - std_color
                    std_dev = np.sqrt(np.mean(rgb_diff ** 2))
                    if std_dev < weight:  # 역치
                        cube_color[j - 1].append(color)
                        break
                    elif color_name.index(color) == len(color_name) - 1:
                        color_dict[str(color_idx)] = center_rgb
                        cube_color[j - 1].append(color_idx)
                        color_name.append(color_idx)
                        color_idx += 1
                        break
            else:
                color_dict[str(color_idx)] = center_rgb
                cube_color[j - 1].append(color_idx)
                color_name.append(color_idx)
                color_idx += 1
    return color_idx, color_name, color_dict, cube_color



while True:
    if cube_color_list[cube_aspect - 1] == 0:
        got_color = False
    else:
        got_color = True
    ret, frame = cap.read()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('u'):  # 'up' 화살표 키
        square_size += 10
        print(square_size)
    elif key == ord('d'):  # 'down' 화살표 키
        square_size -= 10
        print(square_size)

    if not ret:
        break

    # 프레임 크기
    height, width, _ = frame.shape

    # 사각형 위치 설정 (프레임 중앙에 위치하도록)
    square_center = (width // 2, height // 2)
    top_left = (square_center[0] - square_size // 2, square_center[1] - square_size // 2)
    bottom_right = (top_left[0] + square_size, top_left[1] + square_size)

    # 사각형 그리기
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # 격자 그리기
    cell_size = square_size // 3
    for i in range(1, 3):
        # 수평선
        cv2.line(frame, (top_left[0], top_left[1] + i * cell_size), (bottom_right[0], top_left[1] + i * cell_size), (0, 255, 0), 2)
        # 수직선
        cv2.line(frame, (top_left[0] + i * cell_size, top_left[1]), (top_left[0] + i * cell_size, bottom_right[1]), (0, 255, 0), 2)
    # rgb 값 받으면 색 표시 하기
    if got_color:
        for i in range(1,4):
            for j in range(1, 4):
                color_circle = tuple(color_dict[str(cube_color_list[cube_aspect - 1][j - 1][i - 1])])
                color_circle = tuple(map(int, color_circle))
                center_x = top_left[0] + i * cell_size - cell_size // 2
                center_y = top_left[1] + j * cell_size - cell_size // 2
                cv2.circle(frame, (center_x, center_y), 10, color_circle, -1)

    cv2.putText(frame,str(cube_aspect), (20, 20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (255,0,255), 2)
    # 프레임 출력
    cv2.imshow('Resizable Square on Camera', frame)

    # 키 이벤트 처리
    if key == ord('q'):
        break
    elif key == 0x20:  # 'space bar'
        color_idx, color_name, color_dict,cube_color = get_cube_color(color_idx, color_name, color_dict)
        cube_color_list[cube_aspect - 1] = cube_color
        got_color = True
    elif key == ord('1'):
        cube_aspect = 1
    elif key == ord('2'):
        cube_aspect = 2
        got_color = False
    elif key == ord('3'):
        cube_aspect = 3
        got_color = False
    elif key == ord('4'):
        cube_aspect = 4
        got_color = False
    elif key == ord('5'):
        cube_aspect = 5
        got_color = False
    elif key == ord('6'):
        cube_aspect = 6
        got_color = False

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
