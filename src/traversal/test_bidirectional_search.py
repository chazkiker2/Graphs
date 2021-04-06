import unittest
from bidirectional_search import bidi_search as bidirectional_search

test_data_01 = {
    "graph": {
        0: {1, 2},
        1: {0, 2, 3, 4},
        2: {0, 1, 4, 6},
        3: {1, 5},
        4: {1, 2, 5},
        5: {3, 4},
        6: {2},
    },
    "paths": {
        0: {
            0: [[0]],
            1: [[0, 1], ],
            2: [[0, 2], ],
            3: [[0, 1, 3], ],
            4: [[0, 1, 4], [0, 2, 4], ],
            5: [[0, 1, 3, 5], [0, 1, 4, 5], [0, 2, 4, 5], ],
            6: [[0, 2, 6], ],
        },
        1: {
            0: [[1, 0], ],
            1: [[1]],
            2: [[1, 2], ],
            3: [[1, 3], ],
            4: [[1, 4], ],
            5: [[1, 3, 5], [1, 4, 5], ],
            6: [[1, 2, 6], ]
        },
    }
}


class TestCase:
    def __init__(self, assertIn, graph, paths, starting_node):
        self.graph = graph
        self.paths = paths
        self.starting_node = starting_node
        self.assertIn = assertIn

    def make_test_start_to(self, end):
        actual = bidirectional_search(self.graph, self.starting_node, end)
        expected = self.paths[end]
        fail_msg = f"Returned result {actual} was not a valid possibility {expected}"
        self.assertIn(actual, expected, fail_msg)

    def test_valid_zero_to_self(self):
        self.make_test_start_to(0)

    def test_valid_zero_to_one(self):
        self.make_test_start_to(1)

    def test_valid_zero_to_two(self):
        self.make_test_start_to(2)

    def test_valid_zero_to_three(self):
        self.make_test_start_to(3)

    def test_valid_zero_to_four(self):
        self.make_test_start_to(4)

    # @unittest.skip
    def test_valid_zero_to_five(self):
        self.make_test_start_to(5)

    def test_zero_to_six(self):
        self.make_test_start_to(6)


class TestBiDirectionalSearchZeroTo(unittest.TestCase, TestCase):
    def setUp(self) -> None:
        TestCase.__init__(
            self,
            assertIn=self.assertIn,
            graph=test_data_01["graph"],
            starting_node=0,
            paths=test_data_01["paths"][0]
        )


class TestBiDirectionalSearchOneTo(unittest.TestCase, TestCase):
    def setUp(self) -> None:
        TestCase.__init__(
            self,
            assertIn=self.assertIn,
            graph=test_data_01["graph"],
            starting_node=1,
            paths=test_data_01["paths"][1]
        )


if __name__ == '__main__':
    unittest.main()
