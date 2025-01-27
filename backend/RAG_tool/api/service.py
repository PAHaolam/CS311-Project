from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from pathlib import Path
import re
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.tools.product_search_tool import product_search_tool
from src.tools.order_create_tool import raw_order_create_tool
from langchain_core.tools.render import render_text_description
from src.memory import SlotMemory
from src.prompts import REACT_PROMPT
from langchain_core.tools import tool


class ChatbotAssistant:
    def __init__(self):
        self.memory = self.create_chat_memory()
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
        @tool
        def order_create_tool(query_str: str):
            """
            Trả lời những câu hỏi liên quan đến tìm kiếm thông tin về một sản phẩm cụ thể của cửa hàng.
            Giúp thực hiện lên đơn khi đã biết thông tin về sản phẩm mà khách hàng muốn đặt mua
                Những tình huống khi sử dụng công cụ này như:
                - Khách hàng yêu cầu đặt hàng cho sản phẩm cụ thể
                - Khách hàng cung cấp thông tin cần thiết của khách hàng như tên, số điện thoại và địa chỉ
            """
            return raw_order_create_tool(query_str, self.memory)
        
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
        react_prompt = REACT_PROMPT.partial(
            tools=render_text_description(list(self.tools)),
            tool_names=", ".join([t.name for t in self.tools]),
        )
        agent = create_tool_calling_agent(
            llm=llm, tools=self.tools, prompt=react_prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
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
        result = self.agent_executor.invoke(
            input={"input": query}
        )
        result = result["output"]

        match = re.search(r"Final Answer:\s*(.+)", result, re.DOTALL)
        result = match.group(1) if match else result
        
        return result

    
if __name__=="__main__":
    assistant = ChatbotAssistant()

    message = "Xin chào"
    response = assistant.complete(message)

    print(response)
    
