from manimlib import *
import numpy as np

class LiquidSimulation():
    def __init__(self,grid,bounding_box,density=1):

        self.grid = grid

        self.bounding_box = bounding_box

        self.density = density
        self.gravity = -0.1

        self.x_coords = []
        self.y_coords = []

        self.x_velocities = []
        self.y_velocities = []

        self.particle_count = 0

    def create_particles(self):
        x1,y1,x2,y2 = self.grid

        x_points = np.arange(x1, x2 + 1, 1 / self.density)
        y_points = np.arange(y1, y2 + 1, 1 / self.density)

        self.x_coords, self.y_coords = np.meshgrid(x_points, y_points)
        self.x_coords = self.x_coords.flatten()
        self.y_coords = self.y_coords.flatten()

        self.particle_count = len(self.x_coords)

        self.x_velocities = np.zeros(self.particle_count)
        self.y_velocities = np.zeros(self.particle_count)

        return self.x_coords, self.y_coords
    
    def update_particles(self,time_step=1):
        self.y_velocities += self.gravity*time_step
        self.y_coords += self.y_velocities*time_step
        return self.x_coords, self.y_coords

class SquareToCircle(Scene):
    def construct(self):
        grid = [2,2,6,5]
        bounding_box = [0,0,8,8]
        density = 1
        sim = LiquidSimulation(grid,bounding_box,density=density)
        x,y = sim.create_particles()

        points = VGroup()
        for i in range(len(x)):
            point = Dot(point=[x[i],y[i],0.0], color=RED)
            points.add(point)

        def update_frame(points):
            x,y = sim.update_particles(0.1)
            for dot, (xi, yi) in zip(points, zip(x.flatten(), y.flatten())):
                dot.move_to([xi, yi, 0.0])

        
        self.add(points)
        self.play(UpdateFromFunc(points, update_frame), run_time=5, rate_func=linear)
        self.wait()

# sim = LiquidSimulation([2,2,6,5],[0,0,8,8],density=1)
# x,y= sim.create_particles()
# print(x,y)
# x,y = sim.update_particles(0.1)
# print(x,y)
# x,y = sim.update_particles(0.1)
# print(x,y)