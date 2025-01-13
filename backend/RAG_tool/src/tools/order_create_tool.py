from datetime import datetime


def raw_order_create_tool(query_str: str, memory) -> str:
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