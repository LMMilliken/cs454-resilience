"""
Contains the "WhileTrueTransformer" that wraps method-bodys in an while True break statement.
"""
import random
from abc import ABC

import logging as log
from typing import Optional

import libcst._nodes.base
from libcst import CSTNode

from lampion.transformers.basetransformer import BaseTransformer


class WhileTrueTransformer(BaseTransformer, ABC):
    """
    Transformer that wraps method-bodies in an While-True-break Statement.
    To be a bit cautious, while possibly applied everywhere, it is only applied at top-level method-blocks.

    IMPORTANT: This is not identical behaviour to the Java Transformer, as the Python Transformer does not need
    return statements. The Java Transformer needed some extra-hacks as it would maybe create dead branches
    (at least, dead on paper).

    Before:
    > def example():
    >   return 1

    After:
    > def example():
    >   while (True):
    >       return 1
    >       break


    Before:
    > def example2():
    >   name = "World"
    >   print(f"Hello {name}")

    After:
    > def example2():
    >   while (True):
    >       name = "World"
    >       print(f"Hello {name}")
    >       break


    Before:
    > def example3(num):
    >   if num % 2 == 0
    >       print("Even!")
    >   else:
    >       print("Odd!")

    After:
    > def example3(num):
    >   if num % 2 == 0
    >       print("Even!")
    >   else:
    >       while (True):
    >           print("Odd!")
    >           break

    The above added elements have redundant ( ) but I add them intentionally to be careful.
    """

    def __init__(
        self,
        max_tries: int = 50,
        seed: Optional[int] = None,
    ):
        super().__init__(seed=seed)
        self._worked = False
        self.set_max_tries(max_tries)
        log.info("WhileTrueTransformer created (%d Re-Tries)", self.get_max_tries())

    def apply(self, cst_to_alter: CSTNode) -> CSTNode:
        """
        Apply the transformer to the given CST.
        Returns the original CST on failure or error.

        Check the function "worked()" whether the transformer was applied.

        :param cst_to_alter: The CST to alter.
        :return: The altered CST or the original CST on failure.

        Also, see the BaseTransformers notes if you want to implement your own.
        """

        altered_cst = cst_to_alter

        tries: int = 0
        max_tries: int = self.get_max_tries()

        transformer = None

        while (not self._worked) and tries <= max_tries:
            try:
                transformer = self.__WhileTrueWrapper(seed=self.seed)

                altered_cst = altered_cst.visit(transformer)

                self._worked = transformer.applied()
                tries = tries + 1

            except libcst._nodes.base.CSTValidationError:
                # This can happen if we try to add strings and add too many Parentheses
                # See https://github.com/Instagram/LibCST/issues/640
                tries = tries + 1
            except libcst._exceptions.ParserSyntaxError:
                # This can happen in two known cases:
                # 1. Original Code is buggy
                # 2. Transformation accidentally kills layout (e.g. removing indents)
                tries = tries + 1

        if tries == max_tries and not self.worked():
            log.warning("WhileTrueTransformer failed after %i attempts", max_tries)

        if transformer is not None:
            self.node_count = transformer.node_count
        return altered_cst

    def reset(self) -> None:
        """Resets the Transformer to be applied again.

           after the reset all local state is deleted, the transformer is fully reset.

           It holds:
           > a = SomeTransformer()
           > b = SomeTransformer()
           > someTree.visit(a)
           > a.reset()
           > assert a == b
        """
        self._worked = False

    def worked(self) -> bool:
        """
        Returns whether the transformer was successfully applied since the last reset.
        If the transformer cannot be applied for logical reasons it will return false without attempts.

        :returns bool
            True if the Transformer was successfully applied.
            False otherwise.

        """
        return self._worked

    def categories(self) -> [str]:
        """
        Gives the categories specified for this transformer.
        Used only for information and maybe later for filter purposes.
        :return: The categories what this transformer can be summarized with.
        """
        return ["Smell", "Structure"]

    def postprocessing(self) -> None:
        """
        Manages all behavior after application, in case it worked(). Also calls reset().
        """
        self.reset()

    class __WhileTrueWrapper(libcst.CSTTransformer):
        """
        Covers two options:

        1. IntendedBlock: Your normal CodeBlock, most average Case
        2. Simple Statement Suite: inline statement-blocks, without intendation

        Note: The LibCST Library does not like to create the AST elements by themselves
        (it does not have a lot of constructors etc.)
        Hence, we first make a small statement with the right condition, and replace the while-body.
        """

        def __init__(
            self,
            seed: Optional[int] = None,
        ):
            super().__init__()
            self.random = random.Random(seed)
            self.__applied = False
            self.chance = 0.1
            self.node_count = 0

        def visit_node(self, node):
            if not self.__applied:
                self.node_count += 1

        def applied(self):
            return self.__applied

        def leave_SimpleStatementSuite(
                self,
                original_node: "SimpleStatementSuite",
                updated_node: "SimpleStatementSuite",
        ) -> "BaseSuite":
            if not self.__applied and random.random() < self.chance:
                wrapper = libcst.parse_statement("while (True): \n\t return 1")
                breaknode = libcst.parse_statement('break')
                newbody = libcst.Expr(libcst.Module(body = (updated_node, breaknode)))
                wrapper_with_body_changed = wrapper.deep_replace(wrapper.body, newbody)

                self.__applied = True
                return wrapper_with_body_changed
            else:
                # Else case necessary, as the leave_X always needs to return something
                # None-Return will cause exceptions
                return updated_node

        def leave_IndentedBlock(
                self, original_node: "IndentedBlock", updated_node: "IndentedBlock"
        ) -> "BaseSuite":
            if not self.__applied and random.random() < self.chance:
                wrapper = libcst.parse_statement("while (True): \n\t return 1")
                breaknode = libcst.parse_statement('break')
                newbody = libcst.Expr(libcst.Module(body = (updated_node, breaknode)))
                wrapper_with_body_changed = wrapper.deep_replace(wrapper.body, newbody)

                self.__applied = True
                return wrapper_with_body_changed
            else:
                # Else case necessary, as the leave_X always needs to return something
                # None-Return will cause exceptions
                return updated_node
