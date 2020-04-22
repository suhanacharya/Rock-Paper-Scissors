from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class RPSTest(StageTest):
    def generate(self) -> List[TestCase]:
        cases = ["Tim\nrock,gun,lightning,devil,dragon,water,air,paper,sponge,wolf,tree,human,snake,scissors,fire\nrock\npaper\npaper\n!rating\n!exit",
                 "Tim\nrock,paper,scissors\nrock\n!exit",
                 "Tim\nrock,gun,lightning,devil,dragon,water,air,paper,sponge,wolf,tree,human,snake,scissors,fire\nrock\nrock\nrock\nrock\n!exit",
                 "Tim\n\nrock\nrock\nrock\navada_kedavra\nrock\n!exit",
                 "Tim\n1,2,3,4,5\n1\n1\n2\n3\n4\n5\n!exit"]
        return [TestCase(stdin=case, attach=case, files={'rating.txt': 'Tim 1350\nJane 200\nAlex 400'})
                for case in cases]

    def check(self, reply: str, attach) -> CheckResult:

        if "Okay" not in reply:
            return CheckResult.wrong(
                "There is no \"Okay, let's start\" message in this test"
            )

        reply = [r for r in reply.split("\n") if len(r) != 0]
        attach = attach.split("\n")

        if len(reply) == 0:
            return CheckResult.wrong(
                "Looks like you didn't output anything!"
            )



        rating = 1350
        self.options = (attach[1] or "rock,paper,scissors").split(",")
        for rep in range(len(reply)):
            reply_part = reply[rep]
            try:
                attach_part = attach[rep]
                if attach_part == "!exit" or \
                        "Hello" in reply_part or \
                        "Okay" in reply_part or "Bye!" in reply_part:
                    continue
                if attach_part == "!rating":
                    if reply_part.split(":")[-1].strip() != str(rating):
                        return CheckResult.wrong("User rating is wrong :(")
                    continue
                elif "Sorry" in reply_part:
                    result = -1
                    option = reply_part.split()[-1]
                elif "draw" in reply_part:
                    result = 0
                    if '(' not in reply_part or ')' not in reply_part:
                        return CheckResult.wrong(
                            "There are no '(' or ')' character when there is a draw"
                        )
                    start = reply_part.index('(')
                    end = reply_part.index(')')
                    option = reply_part[start + 1: end]
                    rating += 50
                elif "Well" in reply_part:
                    result = 1
                    option = reply_part.split()[-3]
                    rating += 100
                elif "Invalid input" in reply_part:
                    result = 2
                    if attach_part in self.options:
                        return CheckResult.wrong(
                            'Looks like you output "Invalid input" '
                            'in the wrong place'
                        )
                else:
                    raise IndexError

                if attach_part not in self.options:
                    if result == 2:
                        res = True
                    else:
                        return CheckResult.wrong(
                            "Looks like you didn't handle an invalid input correctly"
                        )
                else:
                    res = self.solve(result, attach_part.strip(), option.strip())

                if res is False:
                    return CheckResult.wrong(
                        "You chose " + attach_part + ", "
                        "computer chose " + option + '. '
                        'And the answer was \"' + reply_part + '\". '
                        'That\'s wrong reply'
                    )

                if res < 0:
                    raise IndexError
            except IndexError:
                return CheckResult.wrong("Seems like your answer (\"{}\") does not fit in given templates".format(reply_part))
        return CheckResult.correct()

    def solve(self, result, *options):
        if any(opt not in self.options for opt in options):
            return -1
        diff = self.options.index(options[0]) - self.options.index(options[1])
        if not diff:
            true_result = 0
        else:
            true_result = (-1) ** ((abs(diff) - (len(self.options) // 2) > 0) == (diff > 0))
        return true_result == result

if __name__ == '__main__':
    RPSTest("rps.game").run_tests()
