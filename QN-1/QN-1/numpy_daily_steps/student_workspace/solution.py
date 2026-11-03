import numpy as np

class DailyStepsTracker:
    def __init__(self):
        # Initialize an empty array to store steps
        self.steps = np.array([])

    def create_steps_array(self, steps_list):
        # Convert list of steps to NumPy array
        self.steps = np.array(steps_list)
        return self.steps
        
    def calculate_total_steps(self, steps_array):
        # Add all the values in the array
        total = 0
        for steps in steps_array:
            total += steps
        return total
    pass
    def calculate_average_steps(self, steps_array):
        # Calculate the average of the steps
        if len(steps_array) == 0:
            return 0.0
        total = self.calculate_total_steps(steps_array)
        average = total / len(steps_array)
        return round(average, 1)
    pass
    def days_above_target(self, steps_array, target):
        # Return only the steps that are greater than target
        result = []
        for steps in steps_array:
            if steps > target:
                result.append(steps)
        return np.array(result)