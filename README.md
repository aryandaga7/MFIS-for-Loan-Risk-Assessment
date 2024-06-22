# Mamdani Fuzzy Inference System (MFIS) for Loan Risk Assessment

## Overview

This project involves developing a decision-support system for Banco Pichin to assist in the assessment of personal loan applications. The system is built using a Mamdani Fuzzy Inference System (MFIS) that evaluates the risk associated with loan applications based on various factors such as the applicant's age, income level, assets, loan amount, job stability, and credit history. By leveraging fuzzy logic, the system can handle uncertainties and imprecise inputs, providing a nuanced risk assessment.


## System Components

1. **Fuzzification**: Converts crisp input values into degrees of membership for fuzzy sets. Variables include Age, Income Level, Assets, Amount, Job, and History.

2. **Rule Evaluation**: Uses a set of expert-defined rules provided by Banco Pichin. Each rule consists of antecedents (conditions on the input variables) and a consequent (the resulting risk level).

3. **Aggregation**: Combines the fuzzy sets resulting from the rule evaluations into a single fuzzy set for the risk level.

4. **Defuzzification**: Converts the aggregated fuzzy set into a single crisp risk score using the centroid method.

## Methodology

### Phase 1: Definition of Variables
- Identify key input variables: Age, Income Level, Assets, Amount, Job, and History.
- Create fuzzy sets for each variable with corresponding membership functions.

### Phase 2: Definition of Rules
- Collect expert knowledge to define inference rules.
- Compile rules into a Rules.txt file.

### Phase 3: System Implementation
- Develop the `FuzzySet` and `Rule` classes in Python.
- Implement functions for reading fuzzy sets, rules, and application data from text files.
- Construct the fuzzification, rule evaluation, aggregation, and defuzzification processes.
- Integrate all components into a complete system.

### Phase 4: Testing and Validation
- Test the system with various loan applications to ensure correct risk assessment.
- Validate the system's performance by comparing the output risk scores with expected results.

### Phase 5: Documentation and Delivery
- Prepare the project report detailing the system, methodology, and results.
- Create a video presentation explaining the project and demonstrating the system.
- Deliver the final package, including source code, results, and analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mfis-loan-risk-assessment.git
