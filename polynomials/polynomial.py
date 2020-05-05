class TermNode:

    def __init__(self, exponent, coefficient):
        self.exponent = exponent
        self.coefficient = coefficient
        self.next = None

    def __eq__(self, TermNode):
        return self.coefficient == TermNode.coefficient and self.exponent == TermNode.exponent

    def __ne__(self, TermNode):
        return not self.__eq__(TermNode)


class Polynomial:
    first_node = TermNode(None, None)

    def __init__(self, exponent, coefficient):

        if exponent is None:
            self.Head = None
        else:
            self.Head = TermNode(exponent, coefficient)

    def __add__(self, Polynomialy):

        newPoly = Polynomial(None, None)
        nodeA = self.Head
        nodeB = Polynomialy.Head
        curr_term = newPoly.Head
        while nodeA is not None and nodeB is not None:
            if nodeB.exponent == nodeA.exponent:
                exponent = nodeA.exponent
                coefficient = nodeA.coefficient + nodeB.coefficient
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeA = nodeA.next
                nodeB = nodeB.next

            elif nodeA.exponent > nodeB.exponent:

                exponent = nodeA.exponent
                coefficient = nodeA.coefficient
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeA = nodeA.next

            else:

                exponent = nodeB.exponent
                coefficient = nodeB.coefficient
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeB = nodeB.next

        while nodeA is not None:
            exponent = nodeA.exponent
            coefficient = nodeA.coefficient
            if newPoly.Head is None:
                newPoly.Head = TermNode(exponent, coefficient)
                curr_term = newPoly.Head
            else:
                curr_term.next = TermNode(exponent, coefficient)
                curr_term = curr_term.next
            nodeA = nodeA.next

        while nodeB is not None:
            exponent = nodeB.exponent
            coefficient = nodeB.coefficient
            if newPoly.Head is None:
                newPoly.Head = TermNode(exponent, coefficient)
                curr_term = newPoly.Head
            else:
                curr_term.next = TermNode(exponent, coefficient)
                curr_term = curr_term.next
            nodeB = nodeB.next

        return newPoly

    def __mul__(self, Polynomialy):
        newPoly = Polynomial(None, None)
        nodeA = self.Head
        nodeB = Polynomialy.Head
        curr_term = newPoly.Head

        while nodeB is not None:
            while nodeA is not None:
                exponent = nodeA.exponent + nodeB.exponent
                coefficient = nodeA.coefficient * nodeB.coefficient
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeA = nodeA.next
            nodeA = self.Head
            nodeB = nodeB.next

        return self.normalization(newPoly)

    def normalization(self, poly):
        nodeA = poly.Head

        while nodeA is not None:
            nodeB = nodeA.next
            if nodeB is not None and nodeA.exponent == nodeB.exponent:
                nodeA.exponent = nodeA.exponent
                nodeA.coefficient = nodeA.coefficient + nodeB.coefficient
                nodeA.next = nodeB.next
            nodeA = nodeA.next

        return poly

    def differentiate(self):
        newPoly = Polynomial(None, None)
        nodeA = self.Head
        curr_term = newPoly.Head

        while nodeA is not None:
            if nodeA.exponent != 0:
                exponent = nodeA.exponent - 1
                coefficient = nodeA.coefficient * nodeA.exponent
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeA = nodeA.next

        return newPoly

    def integrate(self):
        newPoly = Polynomial(None, None)
        nodeA = self.Head
        curr_term = newPoly.Head

        while nodeA is not None:
            if nodeA.exponent != 0:
                exponent = nodeA.exponent + 1
                coefficient = nodeA.coefficient / nodeA.exponent
                if newPoly.Head is None:
                    newPoly.Head = TermNode(exponent, coefficient)
                    curr_term = newPoly.Head
                else:
                    curr_term.next = TermNode(exponent, coefficient)
                    curr_term = curr_term.next
                nodeA = nodeA.next

        return newPoly

    def __str__(self):
        reslt_str = ""
        if self.Head is not None:
            nodeA = self.Head
            while nodeA is not None:
                if nodeA.coefficient < 0:
                    exponent = nodeA.exponent
                    coefficient = nodeA.coefficient
                    if nodeA.exponent == 0:
                        reslt_str += (str(coefficient))

                    else:
                        reslt_str += str(coefficient) + "x^" + str(exponent)

                elif nodeA.coefficient > 0:
                    exponent = nodeA.exponent
                    coefficient = nodeA.coefficient
                    if nodeA.exponent == 0:
                        reslt_str += (str(coefficient))

                    else:
                        reslt_str += "+" + str(coefficient) + "x^" + str(exponent)

                else:
                    coefficient = nodeA.coefficient
                    exponent = nodeA.exponent
                    reslt_str += "+" + "x^" + str(exponent)

                nodeA = nodeA.next

        return reslt_str


def __eq__(self, Polynomial):
    nodeA = self.Head
    nodeB = Polynomial.Head

    while nodeA is not None and nodeB is not None:
        if nodeA.exponent != nodeB.exponent or nodeA.coefficient != nodeB.coefficient:
            result = False
            break

        else:
            nodeA = nodeA.next
            nodeB = nodeB.next
            result = True

    return result


def __ne__(self, Polynomial):
    return not __eq__(self, Polynomial)


poly_1 = Polynomial(coefficient=1, exponent=2)
poly_2 = Polynomial(coefficient=3, exponent=4)
poly_3 = poly_1 + poly_2
print(poly_3)