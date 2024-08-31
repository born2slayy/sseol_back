from openai import OpenAI

def genSolar(api_key, params): 
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    stream = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=[
            {
                "role": "system",
                "content": "패션 업계 바이어가 자신이 원하는 브랜드를 찾기 위한 검색을 할거야. 다음 제공되는 검색어에 연상되는 바이어의 선호도나 취향에 대해 디테일하게 분석하여 한 문장으로 제공해줘.(단순 검색어만 집중하지말고 검색어와 비슷한 느낌을 분석해달란 얘기야) 예를 들어 '당신은 ~~~~~~~~ 이러한 취향을 가지셨군요. 당신의 취향을 바탕으로 브랜드를 추천드리겠습니다.' 이런 형식으로"
            },
            {
                "role": "user",
                "content": f"{params}"
            }
        ],
        stream=True,
    )

    result = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
    
    return result