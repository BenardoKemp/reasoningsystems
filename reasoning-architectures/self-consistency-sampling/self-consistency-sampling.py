# Simplified Self-Consistency Workflow

answers = []

for _ in range(5):
    reasoning_path = generate_reasoning(problem)
    answer = extract_answer(reasoning_path)
    answers.append(answer)

final_answer = most_common(answers)

print(final_answer)