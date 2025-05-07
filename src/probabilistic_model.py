from collections import defaultdict
from Chord import Chord
from Rule import Rule
class ProbabilisticModel:
    def __init__(self):
        self.count_dict = defaultdict(int)
        self.lhs_count_dict = defaultdict(int)
        self.prob_dict = {}

    def fit(self, data):

        for cct in data:
            steps, count_dict, lhs_count_dict = self.parse_leftmost(cct)
        self.prob_dict = self.compute_conditional_probs()

    @staticmethod
    def parse_subtree(subtree):
        if isinstance(subtree, dict):
            label = Chord(subtree['label'])
            child_intervals = [str(label.distance_to(Chord(x['label']))) for x in subtree['children']]
            child_qualities = [Chord(x['label']).quality for x in subtree['children']]
            rule = Rule(label.quality, child_intervals, child_qualities)
            
            return rule

    
    def compute_conditional_probs(self):
        prob_dict = {}
        for rule, count in self.count_dict.items():
            lhs = rule[2][1]
            if self.lhs_count_dict[lhs] == 0:
                print(lhs)
            prob_dict[rule] = count / self.lhs_count_dict[lhs]
        return prob_dict

    @staticmethod
    def make_hashable(d):
        def convert(value):
            if isinstance(value, dict):
                return tuple(sorted((k, convert(v)) for k, v in value.items()))
            elif isinstance(value, list):
                return tuple(convert(v) for v in value)
            else:
                return value

        return tuple(sorted((k, convert(v)) for k, v in d.items()))

    def parse_leftmost(self,tree):
        output = []
        steps = []
        stack = [tree]
        parsed_so_far = []

        while stack:
            current = stack.pop(0)
            if current.get('children'):
                rule = ProbabilisticModel.parse_subtree(current)
                rule_key = rule.make_hashable()
                self.count_dict[rule_key] += 1
                self.lhs_count_dict[rule.lhs()] += 1

            steps.append({
                'current': current['label'],
                'parsed_before': parsed_so_far.copy()
            })

            if current.get('children'):
                stack = current['children'] + stack
            else:
                output.append(current['label'])

            parsed_so_far.append(current['label'])

        return steps, self.count_dict, self.lhs_count_dict
    
    def predict(self, data):
        # Placeholder for prediction logic
        pass

    def train(self, data):
        # Placeholder for training logic
        pass

    def evaluate(self, data):
        # Placeholder for evaluation logic
        pass