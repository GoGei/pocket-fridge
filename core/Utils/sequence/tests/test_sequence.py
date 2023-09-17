from factory import fuzzy
from django.test import TestCase
from ..sequence import Sequence


class SequenceTests(TestCase):
    def test_sequence(self):
        sequence_name = 'test'
        sequence = Sequence(sequence_name=sequence_name)

        self.assertEqual(next(sequence), 1)
        self.assertEqual(next(sequence), 2)
        self.assertEqual(next(sequence), 3)

        sequence2 = Sequence(sequence_name=sequence_name)
        self.assertEqual(next(sequence2), 4)
        self.assertEqual(next(sequence2), 5)
        self.assertEqual(next(sequence), 6)
        self.assertNotEqual(next(sequence), 6)
        self.assertEqual(next(sequence), 8)

        self.assertEqual(sequence.get_last_value(), 8)

    def test_initial_value(self):
        sequence_name = 'test'
        initial_value = 15
        current = initial_value
        sequence = Sequence(sequence_name=sequence_name,
                            initial_value=initial_value)

        self.assertEqual(next(sequence), initial_value)
        current += 1
        self.assertEqual(next(sequence), current)
        current += 1
        self.assertEqual(next(sequence), current)
        current += 1

        sequence2 = Sequence(sequence_name=sequence_name)
        self.assertEqual(next(sequence2), current)
        current += 1
        self.assertEqual(next(sequence2), current)
        current += 1
        self.assertEqual(next(sequence), current)
        current += 1
        self.assertNotEqual(next(sequence), current - 1)
        current += 1
        self.assertEqual(next(sequence), current)

    def test_raise_errors(self):
        self.assertRaises(ValueError, Sequence, sequence_name=None)
        self.assertRaises(ValueError, Sequence, sequence_name=fuzzy.FuzzyText(length=64).fuzz())
