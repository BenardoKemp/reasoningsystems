# Simplified Tree-of-Thoughts Workflow

candidate_thoughts = generate_possible_steps(problem)

scored_paths = []

for thought in candidate_thoughts:
    score = evaluate_reasoning(thought)
    scored_paths.append((thought, score))

best_paths = select_top_paths(scored_paths)

expand(best_paths)