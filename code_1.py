import numpy as np
import skfuzzy as fuzz
import re

class FuzzySet:
    def __init__(self, label, xmin, xmax, a, b, c, d):
        self.label = label
        self.xmin = xmin
        self.xmax = xmax
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def membership(self, x):
        if x <= self.a or x >= self.d:
            return 0.0
        elif self.a < x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b < x <= self.c:
            return 1.0
        elif self.c < x < self.d:
            return (self.d - x) / (self.d - self.c)
        return 0.0

class Rule:
    def __init__(self, name, antecedents, consequent):
        self.name = name
        self.antecedents = antecedents
        self.consequent = consequent

def read_fuzzy_sets(file_path):
    fuzzy_sets = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = re.split(r'[=,\s]+', line.strip())
            var_name = parts[0]
            label = parts[1]
            xmin, xmax, a, b, c, d = map(float, parts[2:])
            if var_name not in fuzzy_sets:
                fuzzy_sets[var_name] = []
            fuzzy_sets[var_name].append(FuzzySet(label, xmin, xmax, a, b, c, d))
    return fuzzy_sets

def read_rules(file_path):
    rules = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = re.split(r'[=,\s]+', line.strip())
            name = parts[0]
            consequent = (parts[1], parts[2])
            antecedents = [(parts[i], parts[i + 1]) for i in range(3, len(parts), 2)]
            rules.append(Rule(name, antecedents, consequent))
    return rules

def read_applications(file_path):
    applications = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = re.split(r'[\s,]+', line.strip())
            try:
                app = {parts[i]: float(parts[i + 1]) for i in range(1, len(parts), 2)}
                applications.append(app)
            except ValueError:
                continue
    return applications

def read_risks(file_path):
    fuzzy_sets = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = re.split(r'[=,\s]+', line.strip())
            var_name = 'Risk'
            label = parts[1]
            xmin, xmax, a, b, c, d = map(float, parts[2:])
            if var_name not in fuzzy_sets:
                fuzzy_sets[var_name] = []
            fuzzy_sets[var_name].append(FuzzySet(label, xmin, xmax, a, b, c, d))
    return fuzzy_sets

def fuzzify(variable, value, fuzzy_sets):
    memberships = {}
    for fset in fuzzy_sets[variable]:
        memberships[fset.label] = fset.membership(value)
    return memberships

def apply_rule(rule, inputs, fuzzy_sets):
    antecedent_values = []
    for (var, label) in rule.antecedents:
        memberships = fuzzify(var, inputs[var], fuzzy_sets)
        antecedent_values.append(memberships[label])
    rule_strength = np.min(antecedent_values)
    return (rule.consequent[1], rule_strength)

def aggregate_rules(rules, inputs, fuzzy_sets):
    consequents = {}
    for rule in rules:
        consequent_label, strength = apply_rule(rule, inputs, fuzzy_sets)
        if consequent_label not in consequents:
            consequents[consequent_label] = []
        consequents[consequent_label].append(strength)
    return consequents

def defuzzify(consequents, fuzzy_sets, output_var):
    aggregated = np.zeros_like(np.arange(fuzzy_sets[output_var][0].xmin, fuzzy_sets[output_var][0].xmax, 0.1))
    for label, strengths in consequents.items():
        max_strength = np.max(strengths)
        for fset in fuzzy_sets[output_var]:
            if fset.label == label:
                mf_values = np.array([fset.membership(x) for x in np.arange(fset.xmin, fset.xmax, 0.1)])
                aggregated = np.fmax(aggregated, np.fmin(max_strength, mf_values))
    return fuzz.defuzz(np.arange(fuzzy_sets[output_var][0].xmin, fuzzy_sets[output_var][0].xmax, 0.1), aggregated, 'centroid')

def evaluate_applications(applications, fuzzy_sets, rules):
    results = []
    for app in applications:
        consequents = aggregate_rules(rules, app, fuzzy_sets)
        risk = defuzzify(consequents, fuzzy_sets, 'Risk')
        results.append(risk)
    return results

if __name__ == '__main__':
    fuzzy_sets = read_fuzzy_sets('InputVarSets.txt')
    fuzzy_sets.update(read_risks('Risks.txt'))
    rules = read_rules('Rules.txt')
    applications = read_applications('Applications.txt')
    
    results = evaluate_applications(applications, fuzzy_sets, rules)
    
    with open('Results.txt', 'w') as f:
        for result in results:
            f.write(f'{result}\n')
    
    print("Evaluation complete. Results saved to Results.txt")
