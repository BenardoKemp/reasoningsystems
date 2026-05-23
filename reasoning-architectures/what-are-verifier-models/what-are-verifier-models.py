# Simplified Verification Workflow

solution = generate_solution(problem)

verification = verify_solution(solution)

if verification == "valid":
    print(solution)
else:
    solution = revise_solution(solution)