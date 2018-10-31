"""
--- Day 20: Particle Swarm ---
Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be
able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then
particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's
position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

Increase the X velocity by the X acceleration.
Increase the Y velocity by the Y acceleration.
Increase the Z velocity by the Z acceleration.
Increase the X position by the X velocity.
Increase the Y position by the Y velocity.
Increase the Z position by the Z velocity.
Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay
closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is
simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity).
Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current
X positions (marked in parentheses), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)
At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will
stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

--- Part Two ---
To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their
positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the
same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>
In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick,
particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?

"""


import re


class Particle(object):
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    @classmethod
    def distance(cls, position):
        return sum(map(abs, position))

    def distance_after_n_cycles(self, n):
        return self.distance(self.position_after_n_cycles(n))

    def position_after_n_cycles(self, n):
        px, py, pz = self.position
        vx, vy, vz = self.velocity
        ax, ay, az = self.acceleration

        npx = px + n * vx + 0.5 * n * (n + 1) * ax
        npy = py + n * vy + 0.5 * n * (n + 1) * ay
        npz = pz + n * vz + 0.5 * n * (n + 1) * az

        return npx, npy, npz


class ParticleSwarm(object):
    def __init__(self):
        self.particles = []

    def load_particles(self, filename):
        pattern = r'<([^>]+)>'
        pattern_obj = re.compile(pattern)

        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                matches = pattern_obj.findall(line.strip())
                self.particles.append(Particle(*[tuple(map(int, m.split(','))) for m in matches]))

    def get_closest_particle(self, cycles):
        closest = float('inf')
        closest_i = None

        for i, p in enumerate(self.particles):
            distance = p.distance_after_n_cycles(cycles)
            if distance < closest:
                closest = distance
                closest_i = i

        return closest_i

    def get_remaining_particles(self, cycles):
        n_of_particles = len(self.particles)
        destroyed = set()

        for cycle in range(1, cycles + 1):
            for i, p in enumerate(self.particles):
                if i in destroyed:
                    continue

                i_destroyed = False
                i_pos = p.position_after_n_cycles(cycle)
                for j in range(i + 1, n_of_particles):
                    if j in destroyed:
                        continue

                    j_pos = self.particles[j].position_after_n_cycles(cycle)
                    if i_pos == j_pos:
                        i_destroyed = True
                        destroyed.add(j)

                if i_destroyed:
                    destroyed.add(i)

        return n_of_particles - len(destroyed)


if __name__ == '__main__':
    swarm = ParticleSwarm()
    swarm.load_particles('day20_input.txt')
    print(swarm.get_closest_particle(10000))  # 300
    print(swarm.get_remaining_particles(50))  # 502
