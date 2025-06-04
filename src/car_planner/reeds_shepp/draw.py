import math

import numpy as np

from utils import *
import reeds_shepp.reeds_shepp as rs


def trace_path_points(path, pose: tuple = (0, 0, 0), turning_radius: float=0.1):
    """
    Compute the trajectory points for a given path (list of reeds_shepp.PathElements).
    Returns a list of (x, y) points representing the trajectory.
    """
    # Initialize starting state: position (0, 0) and heading 0 radians (along positive x-axis)
    x, y, theta = pose
    poses = [pose]  # Start with the initial point
    
    for e in path:
        gear_val = 1 if e.gear == rs.Gear.FORWARD else -1  # Adjust based on actual enum access
        
        if e.steering == rs.Steering.STRAIGHT:  # Replace with actual enum for Steering.STRAIGHT
            # Move straight: distance = gear * parameter
            dist = gear_val * e.param
            steps = int(round(e.param/0.001)) + 1
            steps = 10
            for delta in np.linspace(0, dist, steps):
                x_new = x + delta * math.cos(theta)
                y_new = y + delta * math.sin(theta)
                poses.append((x_new, y_new, theta))

            x, y = x_new, y_new,
            
        else:  # Turning motion (LEFT or RIGHT)
            # Determine radius sign: +1 for LEFT, -1 for RIGHT
            r_val = 1.0 if e.steering == rs.Steering.LEFT else -1.0  # Replace with actual enums

            # Compute circle center relative to current position and heading
            cx = x - r_val * math.sin(theta)
            cy = y + r_val * math.cos(theta)
            cx = x - r_val*turning_radius * math.sin(theta)
            cy = y + r_val*turning_radius * math.cos(theta)
            
            # Combined rotation angle = gear * parameter * radius_sign
            angle_sign = gear_val * r_val
            rot_angle = angle_sign * e.param
            rot_angle = angle_sign * (e.param / turning_radius)

            # Vector from center to current position
            dx = x - cx
            dy = y - cy
            
            # Rotate vector by rot_angle (counterclockwise)
            arc_len = turning_radius*e.param
            steps = int(round(arc_len/0.001)) + 1
            steps = 10
            angles = np.linspace(0, rot_angle, steps)
            cos_rot = np.cos(angles)
            sin_rot = np.sin(angles)
            new_dx = dx * cos_rot - dy * sin_rot
            new_dy = dx * sin_rot + dy * cos_rot
            
            # New position after turning
            x_new = cx + new_dx
            y_new = cy + new_dy

            theta_new = theta + rot_angle  # Update heading
            
            for x2, y2, theta2 in zip(x_new, y_new, theta + angles):
                poses.append((x2, y2, theta2))
            x, y, theta = x_new[-1], y_new[-1], theta_new
    
    return poses
