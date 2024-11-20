# biscuit-manufacturing

## Problem Description

A biscuit manufacturing factory is planning to produce a series of biscuits for Christmas. Using the same roll of dough, the factory aims to create various biscuits of different sizes and shapes. The goal is to maximize biscuit production from a single roll while ensuring the highest possible profit.

To achieve this goal, we have the following information :

- The roll of dough has a predefined rectangular length, referred to as ’LENGTH’, representing a one-dimensional problem.
- The roll may contain irregularities, referred to as defects. Each defect has
    - a position ‘x‘
    - and a class, which could be one of several types (e.g., ’a’, ’b’, ’c’, ...).
- The factory aims to produce a set of biscuits. Each Biscuit can be produced an infinite number of times, and has :
    - a specific size (along the same dimension as the roll)
    - a value (price)
    - and a threshold for the maximum number of defects of each class it can contain (otherwise it cannot be marketed).

A solution is defined as an arrangement of biscuits along the dough roll. For an arrangement (assignment) to be valid, it must satisfy the following conditions :

- Biscuits must be placed at integer positions.
- No overlapping of biscuits is allowed. For example, if you place a biscuit B1 of size 3 at position ‘x=2‘, no other biscuit can be assigned to positions ‘x=3‘ or ‘x=4‘.
- Each biscuit placed must contain fewer defects (or an equal number) of each class than its permitted thresholds. For instance, if biscuit B1 of size 3 is placed at ‘x=2‘, it covers positions 2, 3 and 4. If there are 3 defects of class ’a’ in these positions, but B1’s threshold for class ’a’ is a maximum of 2 defects, then the assignment is invalid.
- The total size of the assigned biscuits must not exceed the length of the dough roll.

The value of a solution is the sum of the individual values of the biscuits placed on the roll. However, any portion of the dough roll without an assigned biscuit incurs a penalty of −1 per position, reflecting the company’s loss from wasted material. This penalty is subtracted from the overall value of the solution.

### Benchmark

For this project, the following assumptions are made :
- The length of the roll of dough is set to 500 units.
- The roll has three classes of defects (’a’, ’b’, and ’c’). The set of defects and their positions on the roll are available in the ’defects.csv’ file.
- The biscuit manufacturing factory aims to produce 4 types of biscuits :
- Biscuit 0 with a length of 4, a value of 3, and maximum allowed defects as {′a′ : 4, ′b′ : 2, ′c′ : 3}
- Biscuit 1 with a length of 8, a value of 12, and maximum allowed defects as {′a′ : 5, ′b′ : 4, ′c′ : 4}
- Biscuit 2 with a length of 2, a value of 1, and maximum allowed defects as {′a′ : 1, ′b′ : 2, ′c′ : 1}
- Biscuit 3 with a length of 5, a value of 8, and maximum allowed defects as {′a′ : 2, ′b′ : 3, ′c′ : 2}

## Project Objectives

This section outlines the primary goals of the project, focusing on a comprehensive understanding and addressing the challenges of the problem.
1. Describe the problem and its challenges.
    - Clearly articulate the problem at hand and identify the specific challenges it presents. This includes describing the problem, outlining the constraints and stating the goals of the project.
2. Formulate and implement the problem using Python.
    - Detail the steps taken to translate the problem into a solvable format using Python. Explain the reasoning behind each step and the motivations for the choices made during implementation.
3. Propose two alternative problem-solving approaches.
    - Present two distinct methods for addressing the problem. Example : Uninformed or Informed search solutions, heuristic methods, local search or constraint satisfaction problem tecnhiques. Provide justification for why each method was selected and how it is relevant for solving the problem.
    - You can provide heuristics or approaches that compute a feasible or optimal solution.
    - Compare the two proposed approaches in terms of performance (execution time, quality of the proposed solution, etc.)
4. Conclusion and reflections :
    - Summarize what this project has contributed to your learning experience. Discuss the challenges encountered during the project and how they were addressed. Reflect on any aspects of the project that were particularly insightful or noteworthy.