"""d-ary max-heap.

A d-ary heap is stored in a flat list. For the node at index i:
    parent(i)   = (i - 1) // d
    children(i) = d*i + 1 ... d*i + d

With d = 2 this is the usual binary heap. A larger d makes the tree shallower
(INSERT sifts up fewer levels) but every EXTRACT-MAX has to look at d children
per level instead of 2.
"""

from __future__ import annotations

from typing import Iterable, List, Optional


class DaryHeap:
    def __init__(self, d: int = 2, items: Optional[Iterable] = None) -> None:
        if d < 2:
            raise ValueError("d must be at least 2")
        self.d = d
        self._a: List = []
        self.comparisons = 0  # number of key comparisons performed so far
        if items is not None:
            for x in items:
                self.insert(x)

    def __len__(self) -> int:
        return len(self._a)

    def __bool__(self) -> bool:
        return bool(self._a)

    def peek(self):
        if not self._a:
            raise IndexError("peek from empty heap")
        return self._a[0]

    def insert(self, x) -> None:
        """INSERT: append at the end, then sift up. O(log_d n)."""
        a, d = self._a, self.d
        a.append(x)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) // d
            self.comparisons += 1
            if a[p] >= x:
                break
            a[i] = a[p]
            i = p
        a[i] = x

    def extract_max(self):
        """EXTRACT-MAX: remove the root, move the last item to the root and
        sift down, always swapping with the largest of the d children.
        O(d * log_d n)."""
        a, d = self._a, self.d
        if not a:
            raise IndexError("extract from empty heap")
        top = a[0]
        last = a.pop()
        n = len(a)
        if n == 0:
            return top
        i = 0
        while True:
            first = d * i + 1
            if first >= n:
                break
            # find the largest child
            best = first
            end = min(first + d, n)
            for c in range(first + 1, end):
                self.comparisons += 1
                if a[c] > a[best]:
                    best = c
            self.comparisons += 1
            if a[best] <= last:
                break
            a[i] = a[best]
            i = best
        a[i] = last
        return top

    def is_valid(self) -> bool:
        """Check the max-heap property (used by the tests)."""
        a, d = self._a, self.d
        return all(a[(i - 1) // d] >= a[i] for i in range(1, len(a)))


if __name__ == "__main__":
    h = DaryHeap(d=3, items=[5, 1, 9, 3, 7, 2])
    print([h.extract_max() for _ in range(len(h))])  # [9, 7, 5, 3, 2, 1]
