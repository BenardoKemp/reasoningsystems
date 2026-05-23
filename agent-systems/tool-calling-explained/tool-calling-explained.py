user_request = "Get latest weather data"

tool_response = weather_api(location="Amsterdam")

final_answer = summarize(tool_response)

print(final_answer)