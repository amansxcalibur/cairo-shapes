import math

class Morph:
    @staticmethod
    def _dist(a, b):
        return math.hypot(b[0] - a[0], b[1] - a[1])

    @staticmethod
    def _midpoint(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    @staticmethod
    def _insert_best_midpoint(src, target_point):
        """
        Insert a midpoint on the src edge whose midpoint
        is closest to target_point.
        """
        n = len(src)
        best_i = 0
        best_d = float("inf")

        for i in range(n):
            a = src[i]
            b = src[(i + 1) % n]
            mid = Morph._midpoint(a, b)
            d = Morph._dist(mid, target_point)

            if d < best_d:
                best_d = d
                best_i = i

        a = src[best_i]
        b = src[(best_i + 1) % n]
        mid = Morph._midpoint(a, b)

        return src[:best_i + 1] + [mid] + src[best_i + 1:]

    @staticmethod
    def equalize_vertices(v1: list, v2: list):
        v1 = list(v1)
        v2 = list(v2)

        # Ensure v1 is smaller
        swapped = False
        if len(v1) > len(v2):
            v1, v2 = v2, v1
            swapped = True

        mapping= {}
        for i in v1:
            min_length = Morph._dist(i, v2[0])
            min_key = v2[0]
            for j in v2:
                new_length =Morph._dist(i, j)
                if min_length> new_length:
                    min_length=new_length
                    min_key = j
            mapping[i] = min_key
        
        midpoints = []
        for idx, i in enumerate(v1):
                a = v1[i]
                b = v1[(i + 1) % len(v1)]
                midpoints.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        for j in v2:
            if j in mapping.values():
                continue
            min_length = Morph._dist(j, midpoints[0])
            min_key = midpoints[0]
            for i in midpoints:
                new_length =Morph._dist(i, j)
                if min_length> new_length:
                    min_length=new_length
                    min_key = j
            mapping[min_key] = j

        v1 = dict.keys()
        v2 = dict.values()
        if swapped:
            return v2, v1
        return v1, v2




    @staticmethod
    def get_intermediate_points(v1: list, v2: list, alpha: float):
        """
        Calculates the position of vertices at a specific point in the morph.
        alpha: 0.0 (fully shape 1) to 1.0 (fully shape 2)
        """
        v1, v2 = Morph.equalize_vertices(v1, v2)
        
        morphed = []
        for p1, p2 in zip(v1, v2):
            # Linear interpolation formula: P = P1 + alpha * (P2 - P1)
            x = p1[0] + (p2[0] - p1[0]) * alpha
            y = p1[1] + (p2[1] - p1[1]) * alpha
            morphed.append((x, y))
            
        return morphed