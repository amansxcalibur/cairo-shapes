import math
from pprint import pprint
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class MorphPoint:
    progress: float
    x: float
    y: float

    def to_tuple(self):
        return (self.x, self.y)


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

        return src[: best_i + 1] + [mid] + src[best_i + 1 :]

    @staticmethod
    def equalize_vertices(v1: list, v2: list):
        v1 = list(v1)
        v2 = list(v2)

        swapped = False
        if len(v1) > len(v2):
            v1, v2 = v2, v1
            swapped = True

        # ---- build candidates FIRST (vertices + midpoints) ----
        candidates = []  # (kind, edge_index, point)

        for i, v in enumerate(v1):
            candidates.append(("vertex", i, v))

        n = len(v1)
        for i in range(n):
            a = v1[i]
            b = v1[(i + 1) % n]
            midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            candidates.append(("midpoint", i, midpoint))

        # ---- assign targets to best candidates ----
        used = set()
        mapping = {}  # (kind, idx) -> target_point

        for target in v2:
            best = None
            best_dist = float("inf")

            for kind, idx, pt in candidates:
                key = (kind, idx)
                if key in used:
                    continue

                d = Morph._dist(pt, target)
                if d < best_dist:
                    best_dist = d
                    best = (kind, idx, pt)

            used.add((best[0], best[1]))
            mapping[(best[0], best[1])] = target

        # ---- materialize new v1 / v2 in correct order ----
        new_v1 = []
        new_v2 = []

        for i, v in enumerate(v1):
            # original vertex
            new_v1.append(v)
            if ("vertex", i) in mapping:
                new_v2.append(mapping[("vertex", i)])

            # midpoint after this edge
            if ("midpoint", i) in mapping:
                a = v
                b = v1[(i + 1) % n]
                midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

                new_v1.append(midpoint)
                new_v2.append(mapping[("midpoint", i)])

        if swapped:
            return new_v2, new_v1
        return new_v1, new_v2

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

    def get_point_at_progress(shape, target_prog):
        """Interpolates a point on a shape's edge at a specific progress."""
        # Ensure progress is wrapped between 0 and 1
        target_prog = target_prog % 1.0

        # Find the two vertices this progress falls between
        # (For production, use bisect.bisect_left for speed)
        for i in range(len(shape)):
            p1 = shape[i]
            p2 = shape[(i + 1) % len(shape)]

            # Standard case
            if p1.progress <= target_prog < (p2.progress if p2.progress > 0 else 1.0):
                return Morph._interpolate(p1, p2, target_prog)

        # Fallback for the very last segment (n-1 to 0)
        return Morph._interpolate(
            shape[-1], MorphPoint(1.0, shape[0].x, shape[0].y), target_prog
        )

    def _interpolate(p1, p2, target_prog):
        # Calculate how far we are between p1 and p2 (0.0 to 1.0)
        seg_len = p2.progress - p1.progress
        if seg_len <= 0:
            return p1  # Avoid div by zero at 1.0/0.0

        local_t = (target_prog - p1.progress) / seg_len

        new_x = p1.x + (p2.x - p1.x) * local_t
        new_y = p1.y + (p2.y - p1.y) * local_t
        return MorphPoint(target_prog, new_x, new_y)

    def create_progress_points(points):
        """Converts [(x,y), (x,y)] to [MorphPoint, MorphPoint]"""
        distances = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]  # Wrap around for closed loop
            dist = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
            distances.append(dist)

        total_perimeter = sum(distances)

        # 2. Assign progress based on cumulative distance
        progress_points = []
        current_dist = 0.0
        for i in range(len(points)):
            prog = current_dist / total_perimeter
            progress_points.append(MorphPoint(prog, points[i][0], points[i][1]))
            current_dist += distances[i]

        return progress_points
    
    # so the old algo goes like this. 
    # triangle ->square
    # cycle 1
    # 0->0
    # 0.33->0.5
    # 0.66->0.25
    # cycle 2
    # 0->0 good
    # 0.33->0.5 good
    # 0.66->0.25 bad

    # then the algo goes
    # prev=0.33->0.5
    # next=1.0->1.0 or 0.75
    # # map to the closest in square progress
    # 0.66->0.75

    # cycle3
    # square list check for unpaired.
    # find s2 0.25
    # prev = 0.0->triangle 0
    # next = 0.5->triangle 0.33
    # check mapping with triangle
    # put point between 0 and 0.33 = 0.16

    def balance_morph_points(v1_mp: List[MorphPoint], v2_mp: List[MorphPoint]) -> List[MorphPoint]:
        # We only need to upscale v1 since v1 <= v2 is guaranteed
        result = list(v1_mp)
        target_count = len(v2_mp)

        while len(result) < target_count:
            max_gap = -1.0
            insert_at = -1

            for i in range(len(result)):
                p1 = result[i]
                p2 = result[(i + 1) % len(result)]

                # Calculate the progress gap, handling the 1.0 -> 0.0 wrap-around
                if p2.progress > p1.progress:
                    gap = p2.progress - p1.progress
                else:
                    # This is the segment closing the loop
                    gap = (1.0 - p1.progress) + p2.progress

                if gap > max_gap:
                    max_gap = gap
                    insert_at = i + 1

            # Get the two points defining the longest side
            start_node = result[insert_at - 1]
            end_node = result[insert_at % len(result)]

            # Calculate midpoint (handling progress wrap-around for the last segment)
            mid_progress = (start_node.progress + (max_gap / 2)) % 1.0
            mid_x = (start_node.x + end_node.x) / 2
            mid_y = (start_node.y + end_node.y) / 2

            new_point = MorphPoint(progress=mid_progress, x=mid_x, y=mid_y)
            
            # Insert the new point to split the longest side
            result.insert(insert_at, new_point)

        return result

    # Instead of searching for every point, find the best SHIFT (Rotation)
    def map_vertices_1_to_1(v1_mp, v2_mp):
        # 1. Find which starting point in v2 is closest to v1[0]
        best_start_idx = 0
        min_total_dist = float('inf')
        
        # Try every possible rotation to find the "least twisted" morph
        for shift in range(len(v2_mp)):
            # Calculate distance between v1[0] and v2[shift]
            d = Morph._dist(v1_mp[0].to_tuple(), v2_mp[shift].to_tuple())
            if d < min_total_dist:
                min_total_dist = d
                best_start_idx = shift
                
        # 2. Map 1:1 based on that rotation
        mapping = []
        for i in range(len(v1_mp)):
            target_idx = (i + best_start_idx) % len(v2_mp)
            mapping.append((v1_mp[i], v2_mp[target_idx]))
            
        return mapping
    
    def get_interpolated(v1, v2, alpha):    
        morphed = []
        for p1, p2 in zip(v1, v2):
            # Linear interpolation formula: P = P1 + alpha * (P2 - P1)
            x = p1[0] + (p2[0] - p1[0]) * alpha
            y = p1[1] + (p2[1] - p1[1]) * alpha
            morphed.append((x, y))

        print()
        print(f"=== {alpha} ===")
        pprint(morphed)

        return morphed
    
    @staticmethod
    def get_winding_order(vertices):
        """Returns True if clockwise, False if counter-clockwise."""
        # Shoelace formula approach
        area = 0
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            area += (p2[0] - p1[0]) * (p2[1] + p1[1])
        return area > 0

    @staticmethod
    def map_vertices(v1: list, v2: list):
        print("\n======================")
        # cycle 1
        if Morph.get_winding_order(v1) != Morph.get_winding_order(v2):
            v2 = v2[::-1]
        swapped = False
        if len(v1) > len(v2):
            v1, v2 = v2, v1
            swapped = True

        mapping: List[Tuple[MorphPoint, MorphPoint]] = []

        # assing progress
        v1_mp: List[MorphPoint] = Morph.create_progress_points(v1)
        v2_mp: List[MorphPoint] = Morph.create_progress_points(v2)

        pprint(v1_mp)
        pprint(v2_mp)

        equalized_v1_mp = Morph.balance_morph_points(v1_mp, v2_mp)

        print("--- equalized ---")
        pprint(equalized_v1_mp)
        pprint(v2_mp)

        print("\n --mapping--\n")
        mapping = Morph.map_vertices_1_to_1(equalized_v1_mp, v2_mp)
        pprint(mapping)

        mapped_v1=[]
        mapped_v2=[]
        for point_1, point_2 in mapping:
            mapped_v1.append(point_1.to_tuple())
            mapped_v2.append(point_2.to_tuple())

        if swapped:
            return mapped_v2, mapped_v1
        return mapped_v1, mapped_v2

        # for vert in v1

        # map
        # v2_map_limit = 0
        # for point_v1 in v1_mp:
        #     vertex_1 = point_v1.to_tuple()

        #     candidates = []
        #     # cycle 2
        #     search_area = v2_mp[v2_map_limit:]
            
        #     for offset, point_v2 in enumerate(search_area):
        #         dist = Morph._dist(vertex_1, point_v2.to_tuple())
        #         # Store (distance, point, original_index)
        #         candidates.append((dist, point_v2, v2_map_limit + offset))

        #     if candidates:
        #         # Find the closest point
        #         best_match = min(candidates, key=lambda x: x[0])
                
        #         min_dist_point = best_match[1]
        #         chosen_index = best_match[2] # This is the index in v2_mp
                
        #         mapping.append((point_v1, min_dist_point))
                
        #         # Update the limit to the next index so we don't look back
        #         v2_map_limit = chosen_index + 1

        # print()
        # pprint(mapping)

        # # cycle 2
        # map_length = len(mapping)
        # for idx, pair in enumerate(mapping):
        #     if idx==0:
        #         prev=pair[1]
        #         next=mapping[idx+1][1]
        #     elif idx==map_length-1:
        #         prev=mapping[idx-1][1]
        #         next=pair[1]
        #     else:
        #         prev=mapping[idx-1][1]
        #         next=mapping[idx+1][1]

        #     print()
        #     pprint(pair)
        #     if prev.progress>next.progress:    
        #         print("==bad==")
        #     else:
        #         print("==good==")

