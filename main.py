from manimlib import *
import numpy as np

class LiquidSimulation():
    def __init__(self,grid,bounding_box,particle_size,density=1):

        self.grid = grid

        self.bounding_box = bounding_box

        self.density = density
        self.gravity = -9.8

        self.x_coords = []
        self.y_coords = []

        self.x_velocities = []
        self.y_velocities = []

        self.particle_count = 0

        self.collision_damp = 0.5

        self.damp = 0.9

        self.particle_size = particle_size

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
        x1,y1,x2,y2 = self.bounding_box
        randomness = np.random.normal(1,0.05,self.particle_count)
        velocity = np.sqrt(self.x_velocities**2 + self.y_velocities**2)

        self.y_velocities *= self.damp
        self.y_velocities += self.gravity*time_step
        next_y_coords = self.y_coords + self.y_velocities*time_step
        collision_mask_y = (next_y_coords > (y2 - self.particle_size)) | (next_y_coords < (y1 + self.particle_size))
        self.y_velocities[collision_mask_y] *= -1 * self.collision_damp * randomness[collision_mask_y]
        self.y_coords += self.y_velocities*time_step

        self.x_velocities *= self.damp
        next_x_coords = self.x_coords + self.x_velocities*time_step
        collision_mask_x = (next_x_coords > (x2 - self.particle_size)) | (next_x_coords < (x1 + self.particle_size))
        self.x_velocities[collision_mask_x] *= -1 * self.collision_damp * randomness[collision_mask_x]
        self.x_coords += self.x_velocities*time_step

        return self.x_coords, self.y_coords

class SquareToCircle(Scene):
    def construct(self):
        grid = [-3,-2,3,2]
        bounding_box = [-8,-4,8,4]
        density = 1
        particle_size = 0.1
        sim = LiquidSimulation(grid,bounding_box,particle_size,density=density)
        x,y = sim.create_particles()

        points = VGroup()
        for i in range(len(x)):
            point = Dot(point=[x[i],y[i],0.0], color=RED, radius=particle_size)
            points.add(point)

        def update_frame(points):
            x,y = sim.update_particles(0.025)
            for dot, (xi, yi) in zip(points, zip(x.flatten(), y.flatten())):
                dot.move_to([xi, yi, 0.0])

        rectangle = Rectangle(width=(bounding_box[2]-bounding_box[0]), height=(bounding_box[3]-bounding_box[1]), color=BLUE)
        rectangle.move_to([0,0,0])
        self.add(rectangle)
        self.add(points)
        self.play(UpdateFromFunc(points, update_frame), run_time=20, rate_func=linear)
        self.wait()

# sim = LiquidSimulation([2,2,6,5],[0,0,8,8],density=1)
# x,y= sim.create_particles()
# print(x,y)
# x,y = sim.update_particles(0.1)
# print(x,y)
# x,y = sim.update_particles(0.1)
# print(x,y)