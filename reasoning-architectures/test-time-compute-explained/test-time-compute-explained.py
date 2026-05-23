candidate_paths = []

for _ in range(5):
    reasoning = generate_reasoning(problem)
    score = evaluate(reasoning)
    candidate_paths.append((reasoning, score))

best_reasoning = select_best(candidate_paths)

print(best_reasoning)