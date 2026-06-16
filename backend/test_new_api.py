# -*- coding: utf-8 -*-
import httpx
import time
import json

api_key = "29ff6dc0478c477ba9de6f8cfa0de8b5.0XX2jGp1vvFyjT6s"
base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
model = "glm-4.7-flash"


def test_normal_call():
    print("=== Testing Normal Call ===")
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "作为一名营销专家，请为智谱AI开放平台创作一个吸引人的口号"}
        ],
        "thinking": {"type": "enabled"},
        "max_tokens": 65536,
        "temperature": 1.0,
    }

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }

    print("Testing model:", model)
    print("API URL:", base_url)
    print("Sending request...")

    retry_delay = 1
    max_retries = 3
    
    try:
        for attempt in range(max_retries):
            client = httpx.Client(timeout=120.0)
            response = client.post(base_url, headers=headers, json=payload)
            print("HTTP Status:", response.status_code)
            
            if response.status_code == 429:
                print("Rate limited. Waiting to retry...")
                time.sleep(retry_delay)
                retry_delay *= 2
                client.close()
                continue
            elif response.status_code == 200:
                data = response.json()
                print("API call successful!")
                if "choices" in data and data["choices"]:
                    content = data["choices"][0]["message"].get("content", "")
                    print("AI Response:", content)
            else:
                print("Response:", response.text[:2000])
            client.close()
            break
    except Exception as e:
        print("Request failed:", type(e).__name__, ":", str(e))


def test_streaming_call():
    print("\n=== Testing Streaming Call ===")
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "作为一名营销专家，请为智谱AI开放平台创作一个吸引人的口号"}
        ],
        "thinking": {"type": "enabled"},
        "stream": True,
        "max_tokens": 65536,
        "temperature": 1.0,
    }

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }

    try:
        with httpx.stream("POST", base_url, headers=headers, json=payload, timeout=120.0) as response:
            print("HTTP Status:", response.status_code)
            if response.status_code == 429:
                print("Rate limited. Try again later.")
                return
            elif response.status_code != 200:
                try:
                    text = response.read().decode('utf-8')
                    print("Response:", text[:2000])
                except:
                    print("Failed to read response")
                return
            
            print("Streaming response:")
            full_content = ""
            for chunk in response.iter_lines():
                if chunk.startswith("data: "):
                    chunk_data = chunk[6:]
                    if chunk_data.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(chunk_data)
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0]["delta"]
                            if "content" in delta:
                                content = delta["content"]
                                print(content, end="", flush=True)
                                full_content += content
                    except json.JSONDecodeError:
                        pass
            print("\n\nStream completed!")
    except Exception as e:
        print("Request failed:", type(e).__name__, ":", str(e))


if __name__ == "__main__":
    test_normal_call()
    test_streaming_call()