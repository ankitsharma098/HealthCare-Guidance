

# Here we demonstrate how an agent can respond to plain text questions with data from an AI model and convert it into a machine readable format.
# Note: the AI model used here is not actually able to verify its information and is not guaranteed to be correct. The purpose of this example is to show how to interact with such a model.
#
# In this example we will use:
# - 'agent': this is your instance of the 'Agent' class that we will give an 'on_interval' task
# - 'ctx': this is the agent's 'Context', which gives you access to all the agent's important functions
# - 'requests': this is a module that allows you to make HTTP requests
#
# To use this example, you will need to provide an API key for OPEN AI: https://platform.openai.com/account/api-keys
# You can define your OPENAI_API_KEY value in the .env file
AI_MODEL_AGENT_ADDRESS="agent1qvkrutvg2eux2vupsky3h5qfumcwaq2yng7ma9zkmmd4cn84w7wuyzr0uq7"
response1=None
if OPENAI_API_KEY == "AIzaSyA1ic_1lLLIBCMcCxQgp4nhs5IDHgB_-n8":
    raise Exception("You need to provide an API key for OPEN AI to use this example")

# Configuration for making requests to OPEN AI 
OPENAI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyA1ic_1lLLIBCMcCxQgp4nhs5IDHgB_-n8"
headers = {
    "Content-Type": "application/json",
}
class Request(Model):
    text: str


class Error(Model):
    text: str



class Data(Model):
    value: float
    unit: str
    timestamp: str
    confidence: float
    source: str
    notes: str

# Send a prompt and context to the AI model and return the content of the completion
def get_completion(context: str, prompt: str, max_tokens: int = 1024):
    data = {
    
        "contents": [
            {
                "parts": [
                {
                    "text": prompt,
                }
                ]
            }
        ],

    }

    try:
        response = requests.post(OPENAI_URL, headers=headers, data=json.dumps(data))
        message = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as ex:
        return None
    # print("Got response from AI model: " +message)
    return message
# Instruct the AI model to retrieve data and context for the data and return it in machine readable JSON format
def get_data(ctx: Context, request: str):
    context = '''    
    You are a helpful agent who can provide answers to questions along with sources and relevant context in a machine readable format.
    m  
    Please follow these guidelines:
    1. Try to answer the question as accurately as possible, using only reliable sources.
    2. Rate your confidence in the accuracy of your answer from 0 to 1 based on the credibility of the data publisher and how much it might have changed since the publishing date.
    3. In the last line of your response, provide the information in the exact JSON format: {"value": value, "unit": unit, "timestamp": time, "confidence": rating, "source": ref, "notes": summary}
        - value is the numerical value of the data without any commas or units
        - unit is the measurement unit of the data if applicable, or an empty string if not applicable
        - time is the approximate timestamp when this value was published in ISO 8601 format
        - rating is your confidence rating of the data from 0 to 1
        - ref is a url where the data can be found, or a citation if no url is available
        - summary is a brief justification for the confidence rating (why you are confident or not confident in the accuracy of the value)
    '''

    response = get_completion(context, request, max_tokens=2048)

    try:
        msg = response
        return msg
    except Exception as ex:
        ctx.logger.exception(f"An error occurred retrieving data from the AI model: {ex}")
        return Error(text="Sorry, I wasn't able to answer your request this time. Feel free to try again.")

# Message handler for data requests sent to this agent
@agent.on_message(model=Request)
async def handle_request(ctx: Context, sender: str, request: Request):
    ctx.logger.info(f"Got request from {sender}: {request.text}")
    global response1
    response1 = get_data(ctx, request.text)
    print(response1)
    @agent.on_interval(5)
    async def ask_question(ctx: Context):
        response = get_data(ctx, request.text)
        ctx.logger.info(f"Asking question to AI model agent: ")
        await ctx.send(AI_MODEL_AGENT_ADDRESS, Request(text=response1))
# @agent.on_interval(5)
# async def ask_question(ctx: Context):
#     # response = get_data(ctx, request.text)
#     # ctx.logger.info(f"Asking question to AI model agent: ")
#     await ctx.send(AI_MODEL_AGENT_ADDRESS, Request(text=response))
