"""
stl.py
Create STL for wordclock baffle

TODO: 
1. The long string should be replaced by logic
"""


from typing import Tuple, Union, Sequence, List

class Coords:
    X = 0
    Y = 1


class Vector:
    """ A class representing a 3d vector. """
    coords: Tuple[float] = None
    def __init__(self, x: Union[float, Sequence[float]] = 0.0, y: float = 0.0, z: float = 0.0):
        if hasattr(x, "__iter__"):
            self.x, self.y, self.z = x
        else:
            self.x = x
            self.y = y
            self.z = z
        self.coords = (self.x, self.y, self.z)


    def add(self, p):
        return Vector(*[this+other for this, other in \
            zip(self.coords, p.coords)])

    def __add__(self, other):
        return self.add(other)

    def __str__(self):
        return f"Vector: ({self.x}, {self.y}, {self.z})"


class Box:
    """ A class representing a box. """
    def __init__(self, origin: Vector, diagonal: Vector) -> None:
        """ Create a new Box. """
        self.origin = origin
        self.diagonal = diagonal
        self.x_min, self.y_min, self.z_min = origin.coords
        top_right = origin + diagonal
        self.x_max, self.y_max, self.z_max = top_right.coords


    def get_neighbor(self, diagonal: Vector, axis: int):
        offset = [0, 0, 0]
        offset[axis] = self.diagonal.coords[axis]
        origin = self.origin + Vector(offset)
        return Box(origin, diagonal)


    def copy_to(self, new_origin: Vector):
        return Box(new_origin, self.diagonal)


    def as_string(self) -> str:
        """
        Turn a box into STL string representation.
        A box contains of six sides (six different outward-pointing normals),
        each consisting of two facets, which consist of three vertices, their order is such that
        it follows right hand rule in relation to the normal vector.
        """

        return f"""
facet normal 0.000000 0.000000 1.000000
outer loop
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal 0.000000 0.000000 1.000000
outer loop
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal 0.000000 -1.000000 0.000000
outer loop
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal 0.000000 -1.000000 0.000000
outer loop
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_min:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_min:.6f}
endloop
endfacet
facet normal -1.000000 0.000000 0.000000
outer loop
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_min:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal -1.000000 0.000000 0.000000
outer loop
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_min:.6f}
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_min:.6f}
endloop
endfacet
facet normal 0.000000 0.000000 -1.000000
outer loop
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_min:.6f}
endloop
endfacet
facet normal 0.000000 0.000000 -1.000000
outer loop
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_min:.6f}
vertex {self.x_min:.6f} {self.y_min:.6f} {self.z_min:.6f}
endloop
endfacet
facet normal 1.000000 0.000000 0.000000
outer loop
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal 1.000000 0.000000 0.000000
outer loop
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_min:.6f} {self.z_min:.6f}
endloop
endfacet
facet normal 0.000000 1.000000 0.000000
outer loop
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_max:.6f}
endloop
endfacet
facet normal 0.000000 1.000000 0.000000
outer loop
vertex {self.x_min:.6f} {self.y_max:.6f} {self.z_min:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_max:.6f}
vertex {self.x_max:.6f} {self.y_max:.6f} {self.z_min:.6f}
endloop
endfacet
"""


class Feature:
    """ A Feature is a connected set of Boxes. """
    def __init__(self, origin: Vector, along: int, thickness: float,
                 lengths: Sequence[float], heights: Sequence[float]) -> None:
        self.origin = origin
        self.along = along
        self.lengths = lengths
        self.heights = heights
        self.thickness = thickness
        self.boxes: List[Box] = self._build_array()


    def _perpendicular_from(self, point: Vector, distance: float) -> Vector:
        """ Get Vector of point at given distance in perpendicular direction from given point """
        if self.along == Coords.X:
            return point + Vector(0.0, distance, 0.0)
        elif self.along == Coords.Y:
            return point + Vector(distance, 0.0, 0.0)
        else:
            raise ValueError("axis must be 0 or 1!")


    def duplicate_n_times(self, n: int, spacing: float):
        origins = [self._perpendicular_from(self.origin, i * spacing) for i in range(1, n+1)]

        return [Feature(origin, self.along, self.thickness, self.lengths, self.heights) \
            for origin in origins]


    def _get_offset(self, length: float, height: float) -> Vector:
        if self.along == Coords.X:
            return Vector(length, self.thickness, height)
        elif self.along == Coords.Y:
            return Vector(self.thickness, length, height)
        else:
            raise ValueError("axis must be 0 or 1!")

    
    def _build_array(self) -> Sequence[Box]:
        boxes: List[Box] = []
        last_box = None
        for length, height in zip(self.lengths, self.heights):
            offset = self._get_offset(length, height)
            if last_box is None:
                last_box = Box(self.origin, offset)
            else:
                last_box = last_box.get_neighbor(offset, self.along)
            boxes.append(last_box)
            
        return boxes
        

class Solid:
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._boxes: List[Box] = []


    def add(self, thing: Union[Box, Sequence[Box], Feature, Sequence[Feature]]) -> None:
        if isinstance(thing, (list, tuple)):
            for b in thing:
                if isinstance(b, Feature):
                    self._boxes += b.boxes
                else:
                    self._boxes.append(b)
        else:
            if isinstance(thing, Feature):
                self._boxes += thing.boxes
            else:
                self._boxes.append(thing)


    def move_by(self, x_move: float, y_move: float) -> None:
        for box in self._boxes:
            box.x_min += x_move
            box.x_max += x_move
            box.y_min += y_move
            box.y_max += y_move


    def write(self) -> None:
        with open(self._filename, "w") as file:
            file.write("solid")
            for box in self._boxes:
                file.write(box.as_string() + "\n")
            file.write("endsolid")
