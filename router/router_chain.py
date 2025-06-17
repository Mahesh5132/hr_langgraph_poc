### --- hr_langgraph_poc/router/router_chain.py ---
from langchain.prompts import PromptTemplate
from langchain.chains.router import LLMRouterChain
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

router_prompt = PromptTemplate.from_template("""
Classify the following request into one of: payslip, grievance, appraisal.
Request: {input}
Category:
""")

router_chain = LLMRouterChain.from_llm(llm=llm, prompt=router_prompt)

def get_intent(user_input):
    result = router_chain.run({"input": user_input})
    return result.get("destination", "grievance")


