# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import pyodbc

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionQueryDrinks(Action):
    def name(self) -> Text:
        return "action_query_drinks"
        
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Kết nối đến SQL Server --- DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-FU5UG1UP;DATABASE=E-Commerce_Coffee_And_Tea;UID=sa;PWD=123456"
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=E-Commerce_Coffee_And_Tea;"
                "UID=sa;"
                "PWD=123456;"
            )
            cursor = conn.cursor()
        except pyodbc.Error as e:
            dispatcher.utter_message(text=f"Không thể kết nối cơ sở dữ liệu: {str(e)}")
            return []
        
        # Truy vấn thông tin sản phẩm
        query = "SELECT sp.tenSP, s.tenSize, ct.donGia  FROM SanPham sp, ChiTietSanPham ct, Size s WHERE sp.maSP = ct.maSP AND ct.maSize = s.maSize AND spNoiBat = 1 AND s.tenSize = 'L'"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Tạo danh sách đồ uống để trả lời
        if rows:
            message = "<span class='font-bold'>Danh sách đồ uống nổi bật:</span></br>"
            for row in rows:
                message += f"- {row[0]} ({row[1]}): {row[2]}đ</br>"
        else:
            message = "Hiện không có đồ uống nào!"

        # Gửi thông tin tới người dùng
        dispatcher.utter_message(text=message)
        
        # Đóng kết nối
        conn.close()

        return []
    
class ActionQueryCategories(Action):

    def name(self) -> Text:
        return "action_query_categories"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Kết nối đến SQL Server --- DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-FU5UG1UP;DATABASE=E-Commerce_Coffee_And_Tea;UID=sa;PWD=123456"
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=E-Commerce_Coffee_And_Tea;"
                "UID=sa;"
                "PWD=123456;"
            )
            cursor = conn.cursor()
        except pyodbc.Error as e:
            dispatcher.utter_message(text=f"Không thể kết nối cơ sở dữ liệu: {str(e)}")
            return []
        
        # Truy vấn thông tin sản phẩm
        query = "SELECT tenDM FROM DanhMuc"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Tạo danh mục để trả lời
        if rows:
            message = ""
            for row in rows:
                message += f"- {row[0]}</br>"
        else:
            message = "Hiện không có danh mục nào!"

        # Gửi thông tin tới người dùng
        dispatcher.utter_message(text=message)
        
        # Đóng kết nối
        conn.close()

        return []