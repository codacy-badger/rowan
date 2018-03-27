"""Test function to rotate vector onto vector"""
from __future__ import division, print_function, absolute_import

import unittest
import numpy as np

import hamilton as quaternion


class TestVectorVector(unittest.TestCase):
    def test_simple(self):
        """Test finding quaternion to rotate a vector onto another vector"""
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])
        vec3 = np.array([0, 0, 1])
        quat = quaternion.vector_vector_rotation(vec1, vec2)
        self.assertTrue(
                np.allclose(
                    quat,
                    np.array([[0, np.sqrt(2)/2, np.sqrt(2)/2, 0]])
                    ))
        quat = quaternion.vector_vector_rotation(vec1, vec3)
        self.assertTrue(
                np.allclose(
                    quat,
                    np.array([[0, np.sqrt(2)/2, 0, np.sqrt(2)/2]])
                    ))

    def test_broadcast(self):
        """Test broadcasting"""
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])
        vec3 = np.array([0, 0, 1])

        arr1 = np.stack((vec2, vec3), axis=0)

        output = np.array(
                    [[0, np.sqrt(2)/2, np.sqrt(2)/2, 0],
                     [0, np.sqrt(2)/2, 0, np.sqrt(2)/2]]
                )

        # Test both directions of single array broadcasting
        quat = quaternion.vector_vector_rotation(vec1, arr1)
        self.assertTrue(
                np.allclose(
                    quat,
                    output
                    ))

        quat = quaternion.vector_vector_rotation(arr1, vec1)
        self.assertTrue(
                np.allclose(
                    quat,
                    output
                    ))

        # Matching sizes
        arr2 = np.stack((vec1, vec1), axis=0)
        quat = quaternion.vector_vector_rotation(arr1, arr2)
        self.assertTrue(
                np.allclose(
                    quat,
                    output
                    ))

        # Proper broadcasting
        arr1 = np.stack((vec2, vec3), axis=0)[:, np.newaxis, ...]
        arr2 = np.stack((vec1, vec1), axis=0)[np.newaxis, ...]
        bcast_output = output[:, np.newaxis, ...].repeat(2, axis=1)

        quat = quaternion.vector_vector_rotation(arr1, arr2)
        self.assertTrue(
                np.allclose(
                    quat,
                    bcast_output
                    ))