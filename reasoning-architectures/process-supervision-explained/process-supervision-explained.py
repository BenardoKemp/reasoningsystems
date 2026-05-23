reasoning_steps = generate_reasoning(problem)

evaluation = evaluate_reasoning_steps(reasoning_steps)

if evaluation == "valid":
    final_answer = extract_answer(reasoning_steps)
    print(final_answer)