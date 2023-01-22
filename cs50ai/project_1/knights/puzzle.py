from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A character is either a knight or a knave
    Or(AKnight,AKnave),
    # A says theyre both a knight and a knave
    Implication(AKnight, And(AKnight,AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Each character is a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # If A tells the truth, both caracters are Knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A lies, then they're not both knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #Each character is a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # A says they're the same kind
    #    If A tells the truth, they're both knights
    Implication(AKnight, And(BKnight, AKnight)),
    #    If A lies, then B is a knight and A is a knave
    Implication(AKnave, And(BKnight, AKnave)),
    # B Says they're different Kinds
    Implication(BKnight, And(BKnight, AKnave)),
    Implication(BKnave, Not(And(BKnight, AKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #Each character is a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # A says they're a knight or a knave, but we don't know which
    Implication(AKnight, Or(AKnight,AKnave)),
    # B says that A said that B is a knave
    Implication(BKnight, Implication(AKnave, BKnave)),
    Implication(BKnave, Implication(AKnight, BKnave)),
    # B says that C is a knave
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # C says that A is a Knight
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
