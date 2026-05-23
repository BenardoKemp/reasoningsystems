# Simplified Reflection Loop

response = generate_solution(problem)

feedback = evaluate_response(response)

if feedback == "needs_revision":
    response = revise_solution(response)

print(response)