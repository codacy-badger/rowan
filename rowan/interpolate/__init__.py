# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
R"""
The rowan package provides a simple interface to slerp, the standard method
of quaternion interpolation for two quaternions.
"""

from ..functions import power, multiply, conjugate, _validate_unit, log, norm

__all__ = []


def slerp(q0, q1, t, ensure_shortest=True):
    R"""Linearly interpolate between p and q.

    The `slerp formula <https://en.wikipedia.org/wiki/Slerp#Quaternion_Slerp>`_
    can be easily expressed in terms of the quaternion exponential (see
    :py:func:`rowan.exp`).

    Args:
        q0 ((...,4) np.array): First set of quaternions
        q1 ((...,4) np.array): Second set of quaternions
        t ((...) np.array): Interpolation parameter :math:`\in [0, 1]`
        ensure_shortest (bool): Flip quaternions to ensure we traverse the
            geodesic in the shorter (:math:`<180\degree`) direction

    Returns:
        An array containing the element-wise interpolations between p and q.

    Example::

        q0 = np.array([[1, 0, 0, 0]])
        q1 = np.array([[np.sqrt(2)/2, np.sqrt(2)/2, 0, 0]])
        interpolate.slerp(q0, q1, 0.5)
    """
    _validate_unit(q0)
    _validate_unit(q1)
    t = np.clip(t)

    q0 = np.asarray(q0)
    q1 = np.array(q1)

    # Ensure that we turn the short way around
    if ensure_shortest:
        cos_theta = np.dot(q0, q1)
        flip = cos_theta < 0
        q1[flip] *= -1

    return multiply(q0, power(multiply(conjugate(q0), q1), t))


def slerp_prime(q0, q1, t, ensure_shortest):
    R"""Compute the derivative of slerp.

    Args:
        q0 ((...,4) np.array): First set of quaternions
        q1 ((...,4) np.array): Second set of quaternions
        t ((...) np.array): Interpolation parameter :math:`\in [0, 1]`
        ensure_shortest (bool): Flip quaternions to ensure we traverse the
            geodesic in the shorter (:math:`<180\degree`) direction

    Returns:
        An array containing the element-wise derivatives of interpolations
        between p and q.

    Example::

        q0 = np.array([[1, 0, 0, 0]])
        q1 = np.array([[np.sqrt(2)/2, np.sqrt(2)/2, 0, 0]])
        interpolate.slerp_prime(q0, q1, 0.5)
    """
    _validate_unit(q0)
    _validate_unit(q1)
    t = np.clip(t)

    q0 = np.asarray(q0)
    q1 = np.array(q1)

    # Ensure that we turn the short way around
    if ensure_shortest:
        cos_theta = np.dot(q0, q1)
        flip = cos_theta < 0
        q1[flip] *= -1

    return multiply(
            multiply(q0, power(multiply(conjugate(q0), q1), t)),
            log(conjugate(q0), q1)
            )


def squad(p, a, b, q, t)
    R"""Cubically interpolate between p and q.

    The SQUAD formula is just a repeated application of Slerp between multiple
    quaternions:

    .. math::
        \begin{equation}
            \textnormal{squad}(p, a, b, q, t) = \textnormal{slerp}(p, q, t)
            \left(\textnormal{slerp}(p, q, t)^{-1}\textnormal{slerp}(a, b, t)
            \right)^{2t(1-t)}
        \end{equation}

    Args:
        p ((...,4) np.array): First endpoint of interpolation
        q ((...,4) np.array): Second endpoint of interpolation
        t ((...) np.array): Interpolation parameter :math:`\in [0, 1]`

    Returns:
        An array containing the element-wise interpolations between p and q.

    Example::

        q0 = np.array([[1, 0, 0, 0]])
        q1 = np.array([[np.sqrt(2)/2, np.sqrt(2)/2, 0, 0]])
        interpolate.squad(q0, q1, 0.5)
    """
    _validate_unit(p)
    _validate_unit(a)
    _validate_unit(b)
    _validate_unit(q)
    t = np.clip(t)

    return slerp(slerp(p, q, t, ensure_shortest=False),
                 slerp(a, b, t, ensure_shortest=False),
                 2*t*(1-t),
                 ensure_shortest=False)
