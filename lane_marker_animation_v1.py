# Current implementation for animating movement of lane markers
lane_marker_move_y += speed * 2
if lane_marker_move_y >= marker_height * 2:
    lane_marker_move_y = 0
