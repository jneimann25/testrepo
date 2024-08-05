"""

You are working for a promising new stock trading startup “Algo-Street”.

You have been tasked with developing a new trading signal that will be incorporated into the automatic trading strategy.
The new metric has been called “stock pressure” which aims to measure the tendency for stocks to regress to previous prices.

 The positive stock pressure measures:
 how many consecutive days before today (not including today) have a higher price.

 The negative stock pressure measures:
 how many consecutive days before today (not including today) have a lower price.
 Notice that only one of the two should be greater than 1.

The Stock Pressure is the positive stock pressure - the negative stock pressure.

So if the positive stock pressure is 0 and the negative stock pressure is 3 the stock pressure is -3.

You will be given daily stock prices for the last N days and must return the list of daily stock pressures for each day.
Below is an example for 1 week of data.

        |   Price   | +Pressure | -Pressure |   Pressure  |
-----------------------------------------------------------------
| Day 1 |   100     |     1     |     1     |    0      |
-----------------------------------------------------------------
| Day 2 |   90      |     2     |     1     |    1      |
-----------------------------------------------------------------
| Day 3 |   95      |     1     |     2     |   -1      |
-----------------------------------------------------------------
| Day 4 |   100     |     1     |     4     |   -3      |
-----------------------------------------------------------------
| Day 5 |   105     |     1     |     5     |   -4      |
-----------------------------------------------------------------
| Day 6 |   110     |     1     |     6     |   -5      |
-----------------------------------------------------------------
| Day 7 |   80      |     7     |     1     |    6      |
-----------------------------------------------------------------

Implement the function to compute stock pressure.

In order to compute positive/negative stock pressure for each stock price
you must find the last day with a lower/higher price

You must use two stacks to solve the problem in O(N) time

Code Author: Jonathan Neimann
"""

def compute_pressure(stock_history: list):
    n = len(stock_history)
    positive_pressure_list = [0] * n
    negative_pressure_list = [0] * n
    
    smaller_price_stack = []
    smaller_day_stack= []
    
    for i in range(n):
        if len(smaller_day_stack) == 0:
            smaller_day_stack.append(i+1)
            smaller_price_stack.append(stock_history[i])
            positive_pressure_list[i] = 1
            
        elif stock_history[i] > smaller_price_stack[-1]:
            positive_pressure_list[i] = (i+1) - smaller_day_stack[-1]
            smaller_day_stack.append(i+1)
            smaller_price_stack.append(stock_history[i])
            
        elif min(smaller_price_stack) >= stock_history[i] < smaller_price_stack[-1]:
            positive_pressure_list[i] = i+1
            smaller_day_stack.append(i+1)
            smaller_price_stack.append(stock_history[i])
            
            
        
        elif stock_history[i] < smaller_price_stack[-1] and len(smaller_price_stack) >= 2:
            while stock_history[i] <= smaller_price_stack[-1]:
                smaller_price_stack.pop()
                smaller_day_stack.pop()
            positive_pressure_list[i] = (i+1) - smaller_day_stack[-1]
            smaller_day_stack.append (i+1)
            smaller_price_stack.append(stock_history[i])
            
        elif stock_history[i] < smaller_price_stack[-1]:
            smaller_day_stack.append (i+1)
            smaller_price_stack.append(stock_history[i])
            positive_pressure_list[i] = i +1
            
    larger_price_stack = []
    larger_day_stack = []
    
    for i in range(n):
        
        if len(larger_day_stack) == 0:
            larger_day_stack.append(i+1)
            larger_price_stack.append(stock_history[i])
            negative_pressure_list[i] = 1
            
        if max(larger_price_stack) <= stock_history[i] and stock_history[i] > larger_price_stack[-1]:
            negative_pressure_list[i] = (i +1) 
            larger_day_stack.append(i+1)
            larger_price_stack.append(stock_history[i])
            
            
        
        elif stock_history[i] > larger_price_stack[-1] and len(larger_price_stack) >=2:
            while stock_history[i] >= larger_price_stack[-1]:
                larger_price_stack.pop()
                larger_day_stack.pop()
            negative_pressure_list[i] = (i+1) - larger_day_stack[-1]
            larger_day_stack.append(i+1)
            larger_price_stack.append(stock_history[i])
            
        elif stock_history[i] < larger_price_stack[-1]:
            negative_pressure_list[i] = (i+1) - larger_day_stack[-1]
            larger_day_stack.append(i+1)
            larger_price_stack.append(stock_history[i])
            
            
        elif stock_history[i] > larger_price_stack[-1]:
            negative_pressure_list[i] = (i +1) 
            larger_price_stack.pop()
            larger_day_stack.pop()
            larger_day_stack.append(i+1)
            larger_price_stack.append(stock_history[i])
            
            
    stock_pressure = [pos - neg for pos, neg in zip(positive_pressure_list, negative_pressure_list)]
    return stock_pressure
            
   


"""
DO NOT EDIT BELOW THIS
Below is the unit testing suite for this file.
It provides all the tests that your code must pass to get full credit.
"""


class TestGeneratePressure:
    def run_unit_tests(self):
        self.test_example()
        self.test_2()
        self.test_3()
        self.test_no_days_provided()
        self.test_large_list()

    def print_test_result(self, test_name, result):
        color = "\033[92m" if result else "\033[91m"
        reset = "\033[0m"
        print(f"{color}[{result}] {test_name}{reset}")

    def test_answer(self, test_name, result, expected):
        if result == expected:
            self.print_test_result(test_name, True)
        else:
            self.print_test_result(test_name, False)
            print(f"Expected: {expected} \nGot:      {result}")

    def test_example(self):
        stock_history = [100, 90, 95, 100, 105, 110, 80]

        result = compute_pressure(stock_history)
        expected_answer = [0, 1, -1, -3, -4, -5, 6]

        self.test_answer("test_example", result, expected_answer)

    def test_2(self):
        stock_history = [80, 74, 75, 90, 120, 81]

        result = compute_pressure(stock_history)
        expected_answer = [0, 1, -1, -3, -4, 2]

        self.test_answer("test_2", result, expected_answer)

    def test_3(self):
        stock_history = [1, 2, 5, 10, 12, 20]

        result = compute_pressure(stock_history)
        expected_answer = [0, -1, -2, -3, -4, -5]

        self.test_answer("test_3", result, expected_answer)

    def test_no_days_provided(self):
        stock_history = []

        result = compute_pressure(stock_history)
        expected_answer = []

        self.test_answer("test_no_days_provided", result, expected_answer)

    def test_large_list(self):
        stock_history = [100, 90, 80, 85, 90, 95, 100, 105, 110, 120, 140, 120, 100, 80]

        result = compute_pressure(stock_history)
        expected_answer = [0, 1, 2, -1, -3, -4, -6, -7, -8, -9, -10, 2, 6, 13]

        self.test_answer("test_large_list", result, expected_answer)


if __name__ == '__main__':
    test_runner = TestGeneratePressure()
    test_runner.run_unit_tests()
