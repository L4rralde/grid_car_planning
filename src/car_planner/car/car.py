import math

import numpy as np

from gridsim.shapes import Rectangle
import gridsim.glutils as GLUtils


class Car:
    def __init__(self, x0: float, y0: float, yaw: float) -> None:
        self.width = 0.1
        self.height = 0.05
        self.rect = Rectangle(x0, y0, self.width, self.height, yaw)
        self.trajectory = None

    def drive(self) -> None:
        if not self.trajectory:
            return
        x, y, yaw = self.trajectory.pop(0)
        self.rect = Rectangle(x, y, self.width, self.height, yaw)

    def reset(self, x0: float, y0: float, yaw: float) -> None:
        self.trajectory = None
        self.rect = Rectangle(x0, y0, self.width, self.height, yaw)

    def draw(self) -> None:
        self.rect.draw(color = (0.16, 0.71, 0.79, 1.0))

    def split(self) -> list:
        upper = 0.25 * self.rect.h * np.array(
            [-math.sin(self.rect.yaw), math.cos(self.rect.yaw)]
        )
        points = [
            self.rect.center + upper, 
            self.rect.center - upper
        ]
        for point in points:
            GLUtils.draw_point(*point, size=5)
        return points

    def collides(self, grid: object) -> None:
        for x, y in self.split():
            if grid.point_collides(x, y):
                return True
        return False

    def trigger(self, trajectory: list, ds: float=0.005) -> None:
        self.trajectory = trajectory

    @property
    def pose(self) -> tuple:
        return *self.rect.center, self.rect.yaw


def interpolate_trajectory(trajectory, ds, orientation_method='tangent'):
    n = len(trajectory)
    if n < 2:
        return trajectory
    
    # Compute cumulative arc lengths
    s = [0.0]
    for i in range(1, n):
        x0, y0, _ = trajectory[i-1]
        x1, y1, _ = trajectory[i]
        dx = x1 - x0
        dy = y1 - y0
        segment_length = math.sqrt(dx*dx + dy*dy)
        s.append(s[-1] + segment_length)
    total_length = s[-1]
    
    # Initialize variables
    new_traj = []
    current_index = 0
    current_fraction = 0.0
    s_current = 0.0
    
    # Add the first point
    x0, y0, theta0 = trajectory[0]
    new_traj.append((x0, y0, theta0 if orientation_method == 'interpolate' else None))
    
    # Resample at intervals of ds
    while s_current < total_length:
        s_target = s_current + ds
        if s_target > total_length:
            break
            
        remaining = ds
        while remaining > 0 and current_index < n-1:
            # Current segment points
            xA, yA, _ = trajectory[current_index]
            xB, yB, _ = trajectory[current_index+1]
            dx_seg = xB - xA
            dy_seg = yB - yA
            seg_length = math.sqrt(dx_seg**2 + dy_seg**2)
            
            # Remaining length in current segment
            remaining_in_seg = seg_length * (1 - current_fraction)
            
            if remaining_in_seg >= remaining:
                # Move within current segment
                current_fraction += remaining / seg_length
                s_current += remaining
                remaining = 0
            else:
                # Move to next segment
                remaining -= remaining_in_seg
                s_current += remaining_in_seg
                current_index += 1
                current_fraction = 0.0
        
        # Interpolate position
        xA, yA, _ = trajectory[current_index]
        xB, yB, _ = trajectory[current_index+1]
        x = xA + current_fraction * (xB - xA)
        y = yA + current_fraction * (yB - yA)
        
        # Interpolate orientation if requested
        if orientation_method == 'interpolate':
            thetaA = trajectory[current_index][2]
            thetaB = trajectory[current_index+1][2]
            diff = thetaB - thetaA
            # Handle angle wrapping
            if diff > math.pi:
                diff -= 2 * math.pi
            elif diff < -math.pi:
                diff += 2 * math.pi
            theta = thetaA + current_fraction * diff
            # Normalize to [-pi, pi]
            if theta > math.pi:
                theta -= 2 * math.pi
            elif theta < -math.pi:
                theta += 2 * math.pi
            new_traj.append((x, y, theta))
        else:
            new_traj.append((x, y, None))
    
    # Add last point if not already included
    last_point = trajectory[-1]
    if not new_traj or (new_traj[-1][0] != last_point[0] or new_traj[-1][1] != last_point[1]):
        if orientation_method == 'interpolate':
            new_traj.append((last_point[0], last_point[1], last_point[2]))
        else:
            new_traj.append((last_point[0], last_point[1], None))
    
    # Compute tangent-based orientations if needed
    if orientation_method == 'tangent':
        m = len(new_traj)
        updated_traj = []
        for i in range(m - 1):
            x_curr, y_curr, _ = new_traj[i]
            x_next, y_next, _ = new_traj[i+1]
            dx = x_next - x_curr
            dy = y_next - y_curr
            theta = math.atan2(dy, dx)
            updated_traj.append((x_curr, y_curr, theta))
        # Handle last point
        if m >= 2:
            x_prev, y_prev, _ = new_traj[m-2]
            x_last, y_last, _ = new_traj[m-1]
            dx = x_last - x_prev
            dy = y_last - y_prev
            theta_last = math.atan2(dy, dx)
            updated_traj.append((x_last, y_last, theta_last))
        else:
            # Single point: use original orientation
            updated_traj.append((new_traj[0][0], new_traj[0][1], trajectory[0][2]))
        new_traj = updated_traj
    
    return new_traj