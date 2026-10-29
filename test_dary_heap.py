import heapq
import random
import unittest

from dary_heap import DaryHeap


class TestDaryHeap(unittest.TestCase):
    def test_invalid_d(self):
        with self.assertRaises(ValueError):
            DaryHeap(1)

    def test_empty(self):
        h = DaryHeap(3)
        self.assertEqual(len(h), 0)
        with self.assertRaises(IndexError):
            h.extract_max()
        with self.assertRaises(IndexError):
            h.peek()

    def test_small(self):
        for d in (2, 3, 4, 5):
            h = DaryHeap(d, [5, 1, 9, 3, 7, 2])
            self.assertEqual(h.peek(), 9)
            self.assertEqual([h.extract_max() for _ in range(len(h))],
                             [9, 7, 5, 3, 2, 1])

    def test_heap_property_after_inserts(self):
        for d in (2, 3, 4):
            h = DaryHeap(d)
            for _ in range(500):
                h.insert(random.randint(-100, 100))
                self.assertTrue(h.is_valid())

    def test_matches_heapq_with_duplicates(self):
        for d in (2, 3, 4):
            data = [random.randint(0, 50) for _ in range(1000)]
            h = DaryHeap(d, data)
            got = [h.extract_max() for _ in range(len(h))]
            self.assertEqual(got, sorted(data, reverse=True))

    def test_mixed_operations_against_reference(self):
        for d in (2, 3, 4):
            h, ref = DaryHeap(d), []
            for _ in range(3000):
                if ref and random.random() < 0.4:
                    self.assertEqual(h.extract_max(), -heapq.heappop(ref))
                else:
                    x = random.randint(0, 10**6)
                    h.insert(x)
                    heapq.heappush(ref, -x)
                self.assertEqual(len(h), len(ref))
            self.assertTrue(h.is_valid())


if __name__ == "__main__":
    unittest.main()
