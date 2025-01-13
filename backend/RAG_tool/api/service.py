from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.tools.product_search_tool import load_product_search_tool
from src.tools.order_create_tool import load_order_create_tool, OrderCreateHandler
from src.agents.memory import SlotMemory


class ChatbotAssistant:
    def __init__(self):
        self.memory = self.create_chat_memory()
        self.order_create_handler = OrderCreateHandler()
        self.tools = self.load_tools()
        self.agent_executor = self.create_agent_executor()

    def create_chat_memory(self):
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        chat_memory = SlotMemory(slot_filling_llm = llm)
        return chat_memory

    def load_tools(self):
        """
        Load default RAG tool.
        """
        product_search_tool = load_product_search_tool()
        order_create_tool = load_order_create_tool([self.order_create_handler], self.memory)
        return [product_search_tool, order_create_tool]

    def create_agent_executor(self):
        """
        Creates and configures an agent for routing queries to the appropriate tools.

        This method initializes and configures an agent for routing queries to specialized tools based on the query type.
        It loads a language model, along with specific tools for tasks such as book search and order create.

        Returns:
            Chain: An instance of Chain configured with the necessary tools and settings.
        """
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        react_prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(
            llm=llm, tools=self.tools, prompt=react_prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=self.memory,
            callbacks=[self.order_create_handler],
            verbose=True
        )

        return agent_executor

    def complete(self, query: str) -> str:
        """
        Generate response for given query.

        Args:
            query (str): The input query.

        Returns:
            str: The response.
        """
        try:
            result = self.agent_executor.invoke(
                input={"input": query}
            )
            return result["output"]
        except KeyboardInterrupt as e:
            inputs = {'input': query}
            outputs = {'output': e.args[0]}
            self.memory.save_context(inputs, outputs)
            return e.args[0]
            
    def check_memory(self):
        """
        Check the current content of the memory.

        Returns:
            dict: The current slots and chat history from memory.
        """
        memory_variables = self.memory.chat_memory.messages
        return memory_variables
    
    def check_slot(self):
        slot = self.memory.current_slots
        return slot

    
if __name__=="__main__":
    assistant = ChatbotAssistant()

    message = "Xin chào tôi là Hảo, tôi muốn tìm truyện Naruto"
    response = assistant.complete(message)

    print(response)

    message = "Tôi muốn đặt cuốn thứ 3"
    response = assistant.complete(message)

    print(response)

    slot = assistant.check_slot()
    print(slot)
    
