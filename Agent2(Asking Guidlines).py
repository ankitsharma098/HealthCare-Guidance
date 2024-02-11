# This agent can ask a question to the AI model agent and display the answer.
# Note: Data returned by the AI model is not guaranteed to be correct. The purpose of this example is to show how to interact with such a model.

# Write your question here
QUESTION = "Hii I have some symptoms of ashtama"

AI_MODEL_AGENT_ADDRESS = "agent1qvt94ll37fzp4v5nykm0vm8pnvtjdhnptsfl4dj5jkajpn5q8d57wc8ntg6"


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

def get_data(ctx :Context,request: str):
    print(request)
@agent.on_interval(5)
async def ask_question(ctx: Context):
    ctx.logger.info(f"Asking question to AI model agent: {QUESTION}")
    await ctx.send(AI_MODEL_AGENT_ADDRESS, Request(text=QUESTION))

@agent.on_message(model=Request)
async def handle_data(ctx: Context, sender: str, request: Request):
    ctx.logger.info(f"Got response from AI model agent: {request.text}")

@agent.on_message(model=Error)
async def handle_error(ctx: Context, sender: str, error: Error):
    ctx.logger.info(f"Got error from AI model agent: {error}")
    

# @agent.on_message(model=Request)
# async def handle_request(ctx: Context, sender: str, request: Request):
#     ctx.logger.info(f"Got request from {sender}: {request.text}")
#     response = get_data(ctx, request.text)
#     await ctx.send(sender, response)
