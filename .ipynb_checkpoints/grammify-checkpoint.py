import google.generativeai as genai
genai.configure(api_key='AIzaSyBs3h8fmVHsPp_z5V6Damp1gOI8gDqTsa8')

def restructure(sentence):
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Make the following sentence gramatically correct, make it sound like an impression from an X-Ray. Make sure it is grammaticslly correct, you may use multiple sentences, but it must absolutely be correct: " + sentence

    response = model.generate_content(prompt)
    return response.text
