import openai
import ast

api_key = os.getenv("API_KEY")

# Start OpenAI client
client = openai.OpenAI(api_key=api_key)



# Function that checks whether OpenAI api key is valid
def api_key_valid():
    try:
        client.models.list()
        return True
    except openai.AuthenticationError:
        return False
    except Exception:
        return False

# A function that takes in information about a port and attempts to find exploits relevant to it
def get_vulnerability(port):
    response = "[]"

    try:


        # send prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[

                    {"role": "system",
                     "content": "You are an assistant that only answers with the name of exploits available in the form of an array, nothing else. Leave to 0 response if there are no noteworthy exploits then return empty list. Make sure the exploit applies for the version of the software."},

                    
                    {"role": "user", "content": str(port)}]
            )



        # store result
        response = ast.literal_eval(response.choices[0].message.content)

    except TypeError:
        print("error: invalid port")
        pass
    except openai.AuthenticationError:
        print("Error: OpenAI api key invalid")
        pass
    return response
