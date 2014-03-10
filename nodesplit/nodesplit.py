import random
from math import sqrt, acos, pi

class Engine():

    def __init__(self, world, lines):
        self.world = world
        self.lines = lines
        self.kink_factor = 0.2
        self.operation_line = []
        self.used_slots = []

    def pick_operation_line(self):
        random.shuffle(self.lines)

        for line in self.lines:
            if (line[2] == False):
                self.operation_line = line
                return

        raise Exception

    def get_midpoint(self, a, b):
        return [
            (a[0] + b[0]) / 2,
            (a[1] + b[1]) / 2,
            (a[2] + b[2]) / 2,
        ]

    def get_free_slot(self):
        random.shuffle(self.world)

        for slot in self.world:
            print("{!r} and {!r}".format(slot, self.used_slots))
            if (slot[3] == False) and (slot not in self.used_slots):
                self.used_slots.append(slot)
                print('retruning')
                return [slot[0], slot[1], slot[2]]

    def get_kink(self, a, b, slot):
        midpoint = self.get_midpoint(a, b)
        a_b_distance = self.get_distance(a, b)
        midpoint_slot_distance = self.get_distance(midpoint, slot)
        kink_distance = a_b_distance * self.kink_factor

        if (kink_distance > midpoint_slot_distance):
            raise Exception

        kink_percentage = kink_distance / midpoint_slot_distance

        kink_vector = [
            (slot[0] - midpoint[0]) * kink_percentage,
            (slot[1] - midpoint[1]) * kink_percentage,
            (slot[2] - midpoint[2]) * kink_percentage,
        ]

        return [
            midpoint[0] + kink_vector[0],
            midpoint[1] + kink_vector[1],
            midpoint[2] + kink_vector[2],
        ]

    def get_distance(self, a, b):
        x, y, z = a
        xx, yy, zz = b
        dx = x - xx
        dy = y - yy
        dz = z - zz

        return sqrt(dx*dx + dy*dy +dz*dz)

    def get_vector(self, a, b):
        return [
            b[0] - a[0],
            b[1] - a[1],
            b[2] - a[2],
        ]

    def dotproduct(self, v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))

    def length(self, v):
        return sqrt(self.dotproduct(v, v))

    def angle(self, v1, v2):
        return acos(self.dotproduct(v1, v2) / (self.length(v1) * self.length(v2)))

    def get_stabiliser_slot(self, kink, slot):
        angle = 2 * pi
        tries = 0

        # World's worst algorithm
        while (angle > (pi / 2)):
            stabiliser_slot = self.get_free_slot()
            vector = self.get_vector(kink, slot)
            stabiliser_vector = self.get_vector(kink, stabiliser_slot)
            angle = self.angle(vector, stabiliser_vector)
            tries += 1
            if (angle > (pi / 2)):
                self.used_slots.pop()
            if (tries > 100):
                raise Exception('Bored. Stopping execution.')

        return stabiliser_slot

    def mark_used_slots(self):
        for slot in self.used_slots:
            for index, world_slot in enumerate(self.world):
                if (slot == world_slot):
                    self.world[index][3] = True

    def update_lines(self, kink, slot, stabiliser_slot1, stabiliser_slot2):
        self.lines.append([self.operation_line[0], kink, True])
        self.lines.append([self.operation_line[1], kink, True])
        self.lines.append([kink, slot, False])
        self.lines.append([kink, stabiliser_slot1, False])
        self.lines.append([kink, stabiliser_slot2, False])
        self.lines.remove(self.operation_line)

    def execute(self):
        self.pick_operation_line()
        slot = self.get_free_slot()
        kink = self.get_kink(self.operation_line[0], self.operation_line[1], slot)
        stabiliser_slot1 = self.get_stabiliser_slot(kink, slot)
        stabiliser_slot2 = self.get_stabiliser_slot(kink, slot)
        self.mark_used_slots()
        self.update_lines(kink, slot, stabiliser_slot1, stabiliser_slot2)
