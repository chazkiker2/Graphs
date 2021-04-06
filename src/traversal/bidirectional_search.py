# Bi-Directional Search
# Operates by running two BFS simultaneously, one from the starting node and one from the destination node
# Each iteration, we'll take one step forward and one step back
# Once the paths overlap, we know we've hit a short path
#
# Queue for FORWARD --- represents the next nodes to visit in the starting_node's BST
# Queue for BACKWARD -- represents the next nodes to visit in the destination_node's BST
def bidi_search(graph, start, destination):
    if start == destination:
        return [start]

    # dictionary of currently active vertices with their corresponding paths.
    active_vert_paths = {
        start: [start],  # path from start to _some_node_
        destination: [destination]  # path from destination node to _some_node_
    }

    # will contain vertices that we've ruled out along the way
    inactive_verts = set()

    # while there are still potential solution paths
    while active_vert_paths:
        # every key in active_vert_paths is an active vertex
        active_verts = list(active_vert_paths.keys())
        # for every active vertex
        for vert in active_verts:
            current_path = active_vert_paths[vert]
            origin = current_path[0]
            current_neighbours = set(graph[vert]) - inactive_verts

            # Check if our neighbours hit an active vertex
            # This would happen once each BFS overlaps
            # If this happens, we have a potential solution path
            for meeting_vertex in current_neighbours.intersection(active_verts):
                # Check that the two paths didn't start at same place.
                # If not, then we've got a path from start to goal.
                if origin != active_vert_paths[meeting_vertex][0]:
                    # Reverse one of the paths.
                    active_vert_paths[meeting_vertex].reverse()
                    # combine the results
                    joined_paths = active_vert_paths[vert] + active_vert_paths[meeting_vertex]
                    # if joined_paths is in reverse order, we'll just reverse it
                    if joined_paths[0] != start:
                        joined_paths.reverse()
                    # return our joined paths from start to end!
                    return joined_paths

            # if we're here, we did not find a solution at this level
            # so check for new neighbours to extend our paths another level
            new_neighbors = set(current_neighbours) - inactive_verts - set(active_verts)
            if new_neighbors:
                # If we have new neighbors — extend the paths, remove the previous one and update the inactive vertices.
                for neighbor_vert in new_neighbors:
                    active_vert_paths[neighbor_vert] = current_path + [neighbor_vert]
                    active_verts.append(neighbor_vert)
                active_vert_paths.pop(vert, None)
                inactive_verts.add(vert)

            else:
                # Otherwise, if no new neighbors, then remove the current path and record the endpoint as inactive.
                active_vert_paths.pop(vert, None)
                inactive_verts.add(vert)


if __name__ == '__main__':
    graph = {
        0: {1, 2},
        1: {0, 2, 3, 4},
        2: {0, 1, 4, 6},
        3: {1, 5},
        4: {1, 2, 5},
        5: {3, 4},
        6: {2},
    }
    zero_to = {
        0: [
            [0]
        ],
        1: [
            [0, 1],
        ],
        2: [
            [0, 2],
        ],
        3: [
            [0, 1, 3],
        ],
        4: [
            [0, 1, 4],
            [0, 2, 4],
        ],
        5: [
            [0, 1, 3, 5],
            [0, 1, 4, 5],
            [0, 2, 4, 5],
        ],
        6: [
            [0, 2, 6],
        ],
    }

    ACTUAL = "actual"
    EXPECTED = "expected"
    RESULT = "result"


    def make_test_case(end):
        test_dict = {
            ACTUAL: bidi_search(graph, 0, end),
            EXPECTED: zero_to[end]
        }
        test_dict[RESULT] = test_dict[ACTUAL] in test_dict[EXPECTED]
        return test_dict


    def make_test_suite(graph_in):
        test_dict = {
            i: {
                ACTUAL: bidi_search(graph_in, 0, i),
                EXPECTED: zero_to[i]
            } for i in range(len(graph_in))
        }
        for i in range(len(graph_in)):
            test_dict[i][RESULT] = test_dict[i][ACTUAL] in test_dict[i][EXPECTED]
        return test_dict


    test_cases_from_zero = make_test_suite(graph_in=graph)
    print('\t' + '\n\t'.join(f"{key} = {value}" for key, value in test_cases_from_zero.items()))
