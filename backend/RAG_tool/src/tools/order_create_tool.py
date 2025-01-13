import sys
from pathlib import Path
from datetime import datetime
from icecream import ic

sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

    
class OrderCreateHandler(BaseCallbackHandler):
    def on_tool_end(self, output, **kwargs):
        if kwargs['name']=='Create a books order' and "xin thêm" in output:
            raise KeyboardInterrupt(output)


def load_order_create_tool(callbacks, memory):    
    def answer_query(query_str: str) -> str:
        """Create a books order."""
        slot = memory.current_slots
        miss_info = []
        if slot["name"] == "null":
            miss_info.append("tên")
        if slot["phone"] == "null":
            miss_info.append("sđt")
        if slot["address"] == "null":
            miss_info.append("địa chỉ")
        if len(miss_info) > 1:
            output = "Cho mình xin thêm "
            output = output + ", ".join(miss_info[:-1])
            output = output + f" và {miss_info[-1]} của bạn để mình tiến hành đặt hàng nhé!"
            return output
        elif len(miss_info) == 1:
            output = f"Cho mình xin thêm {miss_info[0]} để mình tiến hành đặt hàng nhé!"
            return output
        else:
            current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            with open(r"D:\HK5\AIEngineer\CS311_Project\backend\RAG_tool\data\orders.txt", "a", encoding="utf-8") as file:
                # Ghi dòng mới với thời gian và giá trị của slots.current_slots
                file.write(f"{current_time} : {slot}\n")
            return "Mình đã nhận được đầy đủ thông tin của bạn, đơn hàng của bạn đã được đặt thành công!"
    
    return Tool(
        name="Create a books order",
        func=answer_query,
        description="""Create a books order.
        Trả lời những câu hỏi liên quan đến tìm kiếm thông tin về một sản phẩm cụ thể của công công ty.
        Giúp thực hiện lên đơn khi đã biết thông tin về sản phẩm mà khách hàng muốn đặt mua
            Những tình huống khi sử dụng công cụ này như:
            - Khách hàng yêu cầu đặt hàng cho sản phẩm cụ thể
            - Khách hàng cung cấp thông tin cần thiết của khách hàng như tên, số điện thoại và địa chỉ
        """,
        callbacks=callbacks
    )