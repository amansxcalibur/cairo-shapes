import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    # This handles the case where the float is on the left side: 5.0 * point
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def get_distance(self):
        return math.hypot(self.x, self.y)

    def rotate_90(self):
        return Point(-self.y, self.x)

    def rotate_270(self):
        return Point(self.y, -self.x)

    def get_direction(self):
        d = self.get_distance()
        return self / d if d > 0 else Point(0, 0)

    @staticmethod
    def interpolate(p1, p2, t):
        return Point(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)


@dataclass
class Cubic:
    p0: Point  # Start point (on the curve).
    p1: Point  # First control point (off the curve; determines exit tangent at p0).
    p2: Point  # Second control point (off the curve; determines entry tangent at p3).
    p3: Point  # End point (on the curve).

    def reverse(self) -> "Cubic":
        # Reverse the order of points to flip the direction of the curve
        return Cubic(p0=self.p3, p1=self.p2, p2=self.p1, p3=self.p0)

    @staticmethod
    def straight_line(x0, y0, x1, y1):
        p0 = Point(x0, y0)
        p3 = Point(x1, y1)
        # Control points are same as endpoints for a straight line
        return Cubic(p0, p0, p3, p3)

    @staticmethod
    def circular_arc(
        cx: float,
        cy: float,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        is_convex: bool,
    ) -> "Cubic":
        """
        Approximate a circular arc with a single cubic Bezier curve.

        Uses the standard "kappa" approximation, which places the control
        points at a distance of (4/3) x tan(θ/4) x radius along the tangent
        at each endpoint, where θ is the arc's subtended angle.

        Args:
            cx, cy:    Center of the circle.
            x0, y0:    Arc start point (must lie on the circle).
            x1, y1:    Arc end point   (must lie on the circle).
            is_convex: True if this corner is convex (bends outward).
                       False for concave (bends inward). Controls which
                       90° rotation is applied to the radius vectors.

        Returns:
            A Cubic Bezier closely approximating the circular arc from
            (x0, y0) to (x1, y1).
        """
        p0 = Point(x0, y0)
        p3 = Point(x1, y1)
        center = Point(cx, cy)

        # Vectors from center to endpoints
        v0 = p0 - center
        v3 = p3 - center

        # Calculate the angle between the two points, basically angle subtended
        # by the arc. Use the dot product of normalized vectors
        d0 = v0.get_direction()
        d3 = v3.get_direction()
        dot = d0.dot_product(d3)

        # Clamp dot product to avoid math domain errors due to precision
        angle = math.acos(max(-1.0, min(1.0, dot)))

        # Kappa: optimal handle length for the cubic arc approximation.
        # Calculate the handles distance (Kappa)
        kappa = (4.0 / 3.0) * math.tan(angle / 4.0)

        # Place control points tangent to the circle at each endpoint.
        # The tangent at any point on a circle is perpendicular to its radius.
        # For a convex corner the tangent rotates CCW (rotate_90);
        # for a concave corner it rotates CW (rotate_270) to keep the arc
        # on the correct side of the chord
        if is_convex:
            p1 = p0 + v0.rotate_90() * kappa
            p2 = p3 + v3.rotate_90() * -kappa
        else:
            p1 = p0 + v0.rotate_270() * kappa
            p2 = p3 + v3.rotate_270() * -kappa
        return Cubic(p0, p1, p2, p3)
