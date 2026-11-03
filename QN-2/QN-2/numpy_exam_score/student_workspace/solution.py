import numpy as np

class ExamScoreAnalyzer:
    def __init__(self):
        self.scores = np.array([])

    def load_scores(self, score_list):
        self.scores = np.array(score_list)
        return self.scores
    
    def compute_summary(self):
        if self.scores.size == 0:
            return "Average: 0.0, Max: 0, Min: 0"
        avg = np.mean(self.scores)
        max_score = np.max(self.scores)
        min_score = np.min(self.scores)
        return f"Average: {avg:.1f}, Max: {max_score}, Min: {min_score}"

    def get_passing_scores(self):
        return self.scores[self.scores >= 40]

    def assign_grades(self):
        grades = []
        for score in self.scores:
            if score >= 90:
                grades.append('A')
            elif score >= 75:
                grades.append('B')
            elif score >= 60:
                grades.append('C')
            elif score >= 40:
                grades.append('D')
            else:
                grades.append('F')
        return grades
