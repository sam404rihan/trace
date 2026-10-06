"""
# Computational geometry

Almost every geometry problem reduces to one question asked many times: going from
p to q to r, do you turn left, turn right, or go straight? The cross product answers
it exactly with integers. No angles, no floats, no division.

## Use it when
- Points, segments, polygons on a grid: "do these cross", "is this inside", "area of"
- "The smallest fence around all the trees" (convex hull)
- "Most points on one line", or slopes in general

## The one formula
```
cross(o, a, b) = (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
  > 0   o -> a -> b turns left (counterclockwise)
  < 0   turns right (clockwise)
  = 0   the three points are collinear
```
It is also twice the signed area of the triangle o, a, b.

## Built from it
- Polygon area (shoelace): sum cross(origin, p[i], p[i+1]) / 2, take abs
- Segments ab and cd cross when c and d are on opposite sides of ab AND a and b are on
  opposite sides of cd. Collinear and touching cases need a bounding-box check.
- Convex hull (monotone chain): sort points, then build the lower and upper chains,
  popping the last point while it doesn't make a left turn. O(n log n).
- Slopes without floats: the direction (dx, dy) divided by gcd(dx, dy), with a fixed sign.

## Common mistakes
- Using floats for slopes: 1/3 and 2/6 can differ in the last bit
- Forgetting collinear and touching cases in segment intersection
- Keeping collinear points on the hull when the problem wants only corners (or the reverse)
- atan2 sorting when a cross-product comparison would be exact
"""


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()                      # not a left turn: the middle point is inside
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area(poly):
    return abs(sum(cross((0, 0), poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))) / 2


print("turn (0,0)->(4,0)->(4,3):", cross((0, 0), (4, 0), (4, 3)), "(positive: left)")
trees = [(0, 0), (4, 0), (4, 3), (0, 3), (2, 1), (1, 2), (2, 3)]
hull = convex_hull(trees)
print("hull:", hull)
print("fence area:", area(hull))
