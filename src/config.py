class WindowConstants:
    height = 800
    width = 800

    tracking_line_color = "green"
    tracking_line_width = 2

    goal_color = "red"
    goal_x1 = (width // 2) - 10
    goal_y1 = 10
    goal_x2 = (width // 2) + 10
    goal_y2 = goal_y1 + 20

    goal_delta_X = (goal_x2 + goal_x1) / 2
    goal_delta_Y = (goal_y2 + goal_y1) / 2

    goal_list = [
        goal_x1,
        goal_y1,
        goal_x2,
        goal_y2
    ]

    obstacle_color = "grey"
    background_color = "white"

    FPS = 120

    obstacle_List = {
        "rectangle_1": [
            200,
            height / 4,
            width - 200,
            (height / 4) + 15
        ],
        "rectangle_2": [
            0,
            (height / 4) * 2,
            width / 3,
            (height / 4) * 2 + 15
        ],
        "rectangle_3": [
            (width / 3) * 2 + 2,
            (height / 4) * 2,
            width + 2,
            (height / 4) * 2 + 15
        ],
        "rectangle_4": [
            200,
            (height / 4) * 3,
            width - 200,
            (height / 4) * 3 + 15
        ],
        "line_1": [
            0,
            0,
            0,
            height
        ],
        "line_2": [
            0,
            height + 2,
            width,
            height + 2
        ],
        "line_3": [
            width + 2,
            0,
            width + 2,
            height
        ],
        "line_4": [
            0,
            0,
            width,
            0
        ]
    }


class FishConstants:
    start_x = WindowConstants.width // 2
    start_y = WindowConstants.height - 50
    height = 20
    width = 5
    color = "black"
    number_of_fish = 200
    max_velocity = 10
    max_drift = 25
    max_lifespan = 200
