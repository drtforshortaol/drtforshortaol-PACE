import unittest
from copy import deepcopy
from pace.controller import ROOT, load, validate, cycle, within, transition

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

    def test_complete_with_evidence(self):
        result = transition(self.config, self.tasks, "EATERY-R01", "completed", "review:123")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.tasks[0]["evidence"], "review:123")

    def test_failed_with_evidence(self):
        result = transition(self.config, self.tasks, "EATERY-T01", "failed", "test log:456")
        self.assertEqual(result["status"], "failed")

    def test_completion_requires_evidence(self):
        with self.assertRaises(ValueError):
            transition(self.config, self.tasks, "EATERY-R01", "completed", "")

    def test_cannot_complete_twice(self):
        transition(self.config, self.tasks, "EATERY-R01", "completed", "review:123")
        with self.assertRaises(ValueError):
            transition(self.config, self.tasks, "EATERY-R01", "completed", "review:124")

    def test_path_boundaries(self):
        self.assertFalse(within("researcher/x", "research/"))
        self.assertTrue(within("research/x", "research/"))

    def test_prefix_spoof(self):
        self.tasks[0]["scope"] = "research-malicious/x"
        with self.assertRaises(AssertionError): validate(self.config, self.tasks)

if __name__ == "__main__":
    unittest.main()
