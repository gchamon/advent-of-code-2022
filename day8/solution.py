def get_trees_ids(filename):
    with open(filename) as input_fp:
        rows = (line.strip() for line in input_fp)
        trees_ids = [[{"id": (x, y), "height": int(height)} for y, height in enumerate(trees)]
                     for x, trees in enumerate(rows)]
    return trees_ids


def stream_edges(filename):
    trees_ids = get_trees_ids(filename)

    yield from trees_ids
    transposed_edges = zip(*trees_ids)
    yield from transposed_edges
    inverted_edges = (trees[::-1] for trees in trees_ids)
    yield from inverted_edges
    transposed_inverted_edges = zip(*trees_ids[::-1])
    yield from transposed_inverted_edges


def stream_views_from_trees(filename):
    trees_ids = get_trees_ids(filename)
    edge_range = len(trees_ids)
    edge_limits = {0, edge_range - 1}
    flat_trees = (tree for tree_row in trees_ids for tree in tree_row)
    trees_by_ids = {tree["id"]: tree for tree in flat_trees}
    trees_views = ((tree, ((trees_by_ids[(tree["id"][0], y)]
                            for y in range(tree["id"][1] + 1, edge_range)),
                           (trees_by_ids[(x, tree["id"][1])]
                            for x in range(tree["id"][0] + 1, edge_range)),
                           (trees_by_ids[(tree["id"][0], y)]
                            for y in range(tree["id"][1] - 1, -1, -1)),
                           (trees_by_ids[(x, tree["id"][1])]
                            for x in range(tree["id"][0] - 1, -1, -1))))
                   for tree in trees_by_ids.values()
                   if tree["id"][0] not in edge_limits and tree["id"][1] not in edge_limits)

    return trees_views


def ray_trace_edges(edges):
    visible_trees = set()
    for edge in edges:
        max_height = -1
        for tree in edge:
            if tree["height"] > max_height:
                visible_trees.add(tree["id"])
                max_height = tree["height"]
    return visible_trees


def ray_trace_views(views):
    scenic_scores = []
    for view in views:
        tree_pivot, view_edges = view
        view_score = 1
        for edge in view_edges:
            edge_score = 0
            for tree in edge:
                edge_score += 1
                if tree["height"] >= tree_pivot["height"]:
                    break
            view_score *= edge_score
        scenic_scores.append((tree_pivot["id"], view_score))
    return sorted(scenic_scores, key=lambda x: x[1], reverse=True)


def solve_example():
    filename = "day8/example.txt"
    edges = list(stream_edges(filename))
    visible_trees = ray_trace_edges(edges)
    return len(visible_trees), ray_trace_views(stream_views_from_trees(filename))


def first_puzzle_solution():
    edges = stream_edges("day8/puzzle_input.txt")
    visible_trees = ray_trace_edges(edges)
    return len(visible_trees)


def second_puzzle_solution():
    return ray_trace_views(stream_views_from_trees("day8/puzzle_input.txt"))[0][1]
