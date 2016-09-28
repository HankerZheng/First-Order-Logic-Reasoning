# Basic First-order Logic Reasoning
This is a simple first-order logic reasoning program. Given some first-order definite clauses, it will calculate the Boolean value of the query by backward-chaining algorithm.

# Input File Format
1. The first line of the input file contains the query. The query can have three forms:
    - as a fact with a **single** atomic sentence: e.g. `Traitor(Anakin`
    - as several *facts* with **multiple** atomic sentences, seperated by `&&`, e.g. `Knows(Sidious, Pine) && Traitor(Anakin)`
    - as a **single** predicate with **one** unknown variable, e.g. `Traitor(x)`
2. The second line contains an integer *n* specifying the number of clauses in the knowledge base.
3. The remaining lines contain the clauses in the knowledge base, **one per line**. Each clause is written in one of the following forms:
    - as an *implication* of the form `p1 ^ p2 ^ ... ^ pn => q`, whose premise is a conjunction of atomic sentences and whose conclusion is a **single** atomic sentence.
    - as a *fact* with a **single** atomic sentence: `q`. Each atomic sentence is a predicate applied to a certain number of arguments.
4. Notes:
    - && denotes the AND operator. => denotes the implication operator. No other operators besides && and => are used.
    - Variables are denoted by a single lowercase letter.
    - All predicates (such as Secret) and constants (such as Anakin) begin with uppercase letters.
    - All predicate names and constant names consist of only uppercase ('A' to 'Z') or lowercase('a' to 'z') letters. There is no number or symbol (e.g. no '_', '-', etc.) in the names.
    - Query will not contain implication.
    - Argument of a predicate can only be constant or variable. There is no number or compound expression (e.g. no Tells(x, y, Hostile(z)) ).

Below is an example of the input file:
```
Traitor(Anakin)
8
ViterbiSquirrel(x) && Secret(y) && Tells(x, y, z) && Hostile(z) => Traitor(x)
Knows(Sidious, Pine)
Resource(Pine)
Resource(x) && Knows(Sidious, x) => Tells(Anakin, x, Sidious)
Resource(x) => Secret(x)
Enemy(x, USC) => Hostile(x)
ViterbiSquirrel(Anakin)
Enemy(Sidious, USC)
```

# Test-case Generator
Source code in `/mywork/self_test/test_generator.py`. Given a basic knowledge base, the test-case generator would randomly generate certain number of possible queries in `/mywork/self_test/testcases/`.