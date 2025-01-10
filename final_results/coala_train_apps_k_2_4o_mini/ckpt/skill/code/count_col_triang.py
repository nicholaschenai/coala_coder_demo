
def count_col_triang(a):
    from itertools import combinations

    # Step 1: Organize points by color
    color_dict = {}
    for point in a:
        coord, color = point
        if color not in color_dict:
            color_dict[color] = []
        color_dict[color].append(coord)

    # Step 2: Initialize variables for results
    total_points = len(a)
    unique_colors = len(color_dict)
    total_triangles = 0
    triangle_counts = {}

    # Step 3: Calculate triangles for each color
    for color, points in color_dict.items():
        num_points = len(points)
        if num_points < 3:
            triangle_counts[color] = 0
            continue
        
        count = 0
        # Check all combinations of 3 points
        for p1, p2, p3 in combinations(points, 3):
            # Step 4: Check for collinearity using the determinant method
            if (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) != 0:
                count += 1
        
        triangle_counts[color] = count
        total_triangles += count

    # Step 5: Find the color(s) with the maximum number of triangles
    max_triangles = max(triangle_counts.values(), default=0)
    max_colors = sorted([color for color, count in triangle_counts.items() if count == max_triangles])

    # Prepare the final output
    if max_triangles > 0:
        return [total_points, unique_colors, total_triangles, [max_colors[0], max_triangles]]
    else:
        return [total_points, unique_colors, total_triangles, []]

