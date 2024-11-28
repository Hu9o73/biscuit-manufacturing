# Problem Overview

The project involves optimizing the use of a roll of dough with defects to produce biscuits of varying sizes and shapes. The aim is to maximize the total profit from the biscuits while minimizing wastage. Each biscuit has specific requirements and thresholds for the number and type of defects it can tolerate. The solution must determine the optimal arrangement of biscuits along the roll to achieve maximum profitability.

# Key Components of the Problem

1. **Dough Roll:**
    - A one-dimensional strip of dough with a fixed length (500 units).
    - Contains defects at certain positions, each classified into one of three classes: 'a', 'b', or 'c'.

2. **Biscuits:**
    - Four types of biscuits are defined, each with:
        - Length: Determines the number of positions it occupies on the roll.
        - Value: Represents the profit earned by placing one biscuit of that type.
        - Defect Tolerances: Specifies the maximum number of defects of each class ('a', 'b', 'c') that can be present under the biscuit.

3. **Constraints:**
    - Biscuits must not overlap on the roll.
    - Each biscuit can only be placed if the defects within its coverage area are within its specified thresholds.
    - The total length of all placed biscuits must not exceed the length of the dough roll.

4. **Objective:**
    - Maximize the total profit by placing biscuits on the roll. Profit being the sum of the values of all the individual biscuits on the roll.
    - Minimize wastage, as unutilized positions on the roll incur a penalty of -1 per unit.


# Challenges

1. **Defect Management:**
    - Each defect class ('a', 'b', 'c') must be carefully tracked along the roll. Identifying valid positions for biscuits based on defect tolerances is computationally demanding, especially for larger rolls with numerous defects.

2. **Optimization Under Constraints:**
    - The placement of biscuits is a combinatorial optimization problem with overlapping and interdependent constraints:
    - Positioning biscuits to maximize profits.
    - Ensuring defect thresholds are not violated.
    - Avoiding overlap between biscuits.

3. **Penalty for Unused Space:**
    - While maximizing profits from biscuit placement, minimizing wastage is crucial to avoid penalties. This requires careful placement to cover as much of the roll as possible without violating constraints.

4. **Combinatorial Explosion:**
    - The large number of possible arrangements of biscuits and their positions leads to a combinatorial explosion, making exhaustive search infeasible. For example, with four biscuit types and 500 positions, the number of potential arrangements grows exponentially.

5. **Trade-Off Between Biscuit Types:**
    - Biscuits with higher values typically occupy more space, potentially leaving gaps that smaller biscuits cannot fill - Balancing the placement of high-value and smaller biscuits is a key challenge.

6. **Heuristics and Computational Complexity:**
    - Finding an efficient heuristic or algorithm to generate a near-optimal solution is non-trivial, especially under tight constraints. Balancing solution quality with computational efficiency is a critical consideration.

# Goals of the Project

- Maximize Total Value: Arrange biscuits to yield the highest profit while satisfying defect and overlap constraints.
- Minimize Wastage: Reduce the penalty incurred by unused portions of the roll.
- Develop Efficient Algorithms: Propose and compare methods that generate feasible or optimal solutions within reasonable timeframes.