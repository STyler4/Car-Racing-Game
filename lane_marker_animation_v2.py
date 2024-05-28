# Trial implementation for animating movement of lane markers with a fixed animation speed
lane_marker_speed = 2  # Adjust this value for desired animation speed

# Inside the game loop, update the lane marker animation
lane_marker_move_y += lane_marker_speed
if lane_marker_move_y >= marker_height * 2:
    lane_marker_move_y = 0
