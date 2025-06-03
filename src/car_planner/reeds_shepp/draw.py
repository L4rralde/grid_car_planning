import math

import turtle
import numpy as np

from utils import *
import reeds_shepp.reeds_shepp as rs
import gridsim.glutils as GLUtils


# drawing n units (eg turtle.forward(n)) will draw n * SCALE pixels
SCALE = 40

def scale(x):
    """
    Scale the input coordinate(s).
    """
    if type(x) is tuple or type(x) is list:
        return [p * SCALE for p in x]
    return x * SCALE

def unscale(x):
    """
    Unscale the input coordinate(s).
    """
    if type(x) is tuple or type(x) is list:
        return [p / SCALE for p in x]
    return x / SCALE

def draw_path(bob, path):
    """
    Draw the path (list of reeds_shepp.PathElements).
    """
    bob = turtle.Turtle()
    for e in path:
        gear = 1 if e.gear == rs.Gear.FORWARD else -1
        if e.steering == rs.Steering.LEFT:
            bob.circle(scale(1), gear * rad2deg(e.param))
        elif e.steering == rs.Steering.RIGHT:
            bob.circle(- scale(1), gear * rad2deg(e.param))
        elif e.steering == rs.Steering.STRAIGHT:
            bob.forward(gear * scale(e.param))


def trace_path_points(path, pose: tuple = (0, 0, 0)):
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
            x_new = x + dist * math.cos(theta)
            y_new = y + dist * math.sin(theta)
            theta_new = theta  # Heading unchanged
            poses.append((x_new, y_new, theta_new))
            x, y, theta = x_new, y_new, theta_new
            
        else:  # Turning motion (LEFT or RIGHT)
            # Determine radius sign: +1 for LEFT, -1 for RIGHT
            r_val = 1.0 if e.steering == rs.Steering.LEFT else -1.0  # Replace with actual enums
            
            # Compute circle center relative to current position and heading
            cx = x - r_val * math.sin(theta)
            cy = y + r_val * math.cos(theta)
            
            # Combined rotation angle = gear * parameter * radius_sign
            angle_sign = gear_val * r_val
            rot_angle = angle_sign * e.param
            
            # Vector from center to current position
            dx = x - cx
            dy = y - cy
            
            # Rotate vector by rot_angle (counterclockwise)
            cos_rot = np.cos(np.linspace(0, rot_angle, 10))
            sin_rot = np.sin(np.linspace(0, rot_angle, 10))
            new_dx = dx * cos_rot - dy * sin_rot
            new_dy = dx * sin_rot + dy * cos_rot
            
            # New position after turning
            x_new = cx + new_dx
            y_new = cy + new_dy

            theta_new = theta + rot_angle  # Update heading
            
            for x2, y2 in zip(x_new, y_new):
                poses.append((x2, y2, theta_new))
            x, y, theta = x_new[-1], y_new[-1], theta_new
    
    return poses
