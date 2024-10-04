prompt_str = """\
Give me a summary of the table with the following JSON format.

- The table name must be unique to the table and describe it while being concise.
- Do NOT output a generic table name (e.g. table, my_table).

Do NOT make the table name one of the following: {exclude_table_name_list}

Table:
{table_str}

Summary: """

REFINE_PROMPT = """\
You will be given a list of history messages and the current user question.\
Your task is to refine the user question based on the previous user question.\
If the current question is not related to the {num} previous user's questions, please return the original question.
Otherwise, you must use the previous user questions to make the current question more effective summarizing the user's intent.

Example:
History:
- user: Truyện Naruto bên shop giá bao nhiêu?

Question: Vậy truyện Conan thì sao?
After refining: Truyện Conan bên shop giá bao nhiêu?

History:
- user: Truyện Naruto bên shop còn không?

Question: Giá bao nhiêu?
After refining: Truyện Naruto bên shop giá bao nhiêu?
"""

RESTRICT_PROMPT = '''\
If you have retrieved any record of the book relevant to the information, you must return your reponse in the following format:
{"Book_1": "id of book 1", "Book_2": "id of book 2", ..., "Book_n": "id of book n"}
if you do not retrieve any record of the book relevant to the information, you must return your response an empty dict
{}
Other than returning the response in the format I provided, you should return absolutely nothing such as note or explanation for your response


for example:
if user look for Naruto book and you retrieve in database 3 record including\
"Naruto - Tập 1" with id is "0412a256aabe4d269546ce3b99c983dc" and "Naruto - Tập 2" with id is "0aefcd0a0f8e4473b13c536dd8fe240b",\
you must return your response is
{"Book_1": "0412a256aabe4d269546ce3b99c983dc", "Book_2": "0aefcd0a0f8e4473b13c536dd8fe240b"}

if user look for Doraemon book and you do not retrive in database any book relevant to Doraemon,\
you must return your response is {}
'''
