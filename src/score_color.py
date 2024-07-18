import colorsys

def get_color_for_score(score : float):
    # Score is between 0 and 1
    # 1 is green, 0 is red
    unnormalized = colorsys.hsv_to_rgb(score/3, 1, 1)
    return tuple(round(i * 255) for i in unnormalized)

if __name__ == '__main__':
    print(get_color_for_score(0.5))