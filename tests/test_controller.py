import unittest
from copy import deepcopy
from pace.controller import ROOT, load, validate, cycle, within

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.config = load(ROOT / "config/project.json")
        self.tasks = load(ROOT / "state/tasks.json")

    def test_valid(self):
        self.assertTrue(validate(self.config, self.tasks))

    def test_two_assignments(self):
        self.assertEqual({a["worker"] for a in cycle(self.config, self.tasks)["assignments"]}, {"A", "B"})

    def test_idempotent(self):
        self.assertEqual(len(cycle(self.config, self.tasks)["assignments"]), 2)

    def test_duplicate(self):
        self.tasks.append(deepcopy(self.tasks[0]))
        with self.assertRaises(AssertionError): validate(self.config, self.tasks)

    def test_ownership(self):
        self.tasks[0]["worker"] = "B"
        with self.assertRaises(AssertionError): validate(self.config, self.tasks)

    def test_evidence(self):
        self.tasks[0]["status"] = "completed"
        with self.assertRaises(AssertionError): validate(self.config, self.tasks)

    def test_path_boundaries(self):
        self.assertFalse(within("researcher/x", "research/"))
        self.assertTrue(within("research/x", "research/"))

    def test_prefix_spoof(self):
        self.tasks[0]["scope"] = "research-malicious/x"
        with self.assertRaises(AssertionError): validate(self.config, self.tasks)

if __name__ == "__main__":
    unittest.main()
