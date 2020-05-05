from unittest import TestCase

from polynomilas.polynomial import TermNode, Polynomial


class TestTermNode(TestCase):
    def test_eql(self):
        node_1 = TermNode(3, 2)
        node_2 = TermNode(1, 2)
        self.assertEqual(node_1 == node_2, False)

    def test_neql(self):
        node_1 = TermNode(3, 2)
        node_2 = TermNode(1, 2)
        self.assertEqual(node_1 != node_2, True)


class TestPolynomial(TestCase):

    def test_add(self):
        poly_1 = Polynomial(3, 2)
        poly_2 = Polynomial(1, 2)
        poly_3 = poly_1+poly_2

        self.assertEqual(str(poly_3), "+2x^3+2x^1")



    def test_mul(self):
        poly_1 = Polynomial(4, 2) + Polynomial(6, 3)
        poly_2 = Polynomial(2, 3)+ Polynomial(4, 3)
        poly_3 = poly_1 * poly_2

        self.assertEqual(str(poly_3), "+9x^10+15x^8+6x^6")

    def test_differentiate(self):
        poly_1 = Polynomial(4, 8)
        self.assertEqual(str(poly_1.differentiate()), "+32x^3")

    def test_integrate(self):
        poly_1 = Polynomial(4, 8)
        self.assertEqual(str(poly_1.integrate()), "+2.0x^5")

    def test_str(self):
        poly_1 = Polynomial(4, 8)
        self.assertEqual(str(poly_1), "+8x^4")

    def test_eq(self):
        poly_1 = Polynomial(3, 2)
        poly_2 = Polynomial(1, 2)
        self.assertEqual(poly_1 == poly_2, False)

    def test_ne(self):
        poly_1 = Polynomial(3, 2)
        poly_2 = Polynomial(1, 2)
        self.assertEqual(poly_1 != poly_2, True)