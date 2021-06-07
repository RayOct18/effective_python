from collections.abc import Sequence


class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class IndexableNode(BinaryTree, Sequence):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()
    
    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')
    
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count

if __name__ == '__main__':
    tree = IndexableNode(
        10,
        left=IndexableNode(
            5,
            left=IndexableNode(2),
            right=IndexableNode(
                6,
                right=IndexableNode(7)
            )
        ),
        right=IndexableNode(
            15,
            left=IndexableNode(11)
        )
    )
    print('Index of 7 is', tree.index(7))
    print('Count of 10 is', tree.count(10))
    print('Tree len is', len(tree))