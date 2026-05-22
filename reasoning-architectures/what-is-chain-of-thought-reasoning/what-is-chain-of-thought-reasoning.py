prompt = """
Question:
A train travels 60 miles in 2 hours.
What is its average speed?

Let's think step-by-step.
"""

response = model.generate(prompt)

print(response)