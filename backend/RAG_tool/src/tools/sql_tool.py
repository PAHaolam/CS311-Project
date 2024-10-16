import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from llama_index.core.tools import FunctionTool

from src.agents.sql_query_pipeline import SQLQueryPipeline


def load_sql_tool():
    qp = SQLQueryPipeline()

    def answer_query(query_str: str) -> str:
        """
        A helpfull function to answer a book query.

        Args:
            query_str (str): The query string to search for.

        Returns:
            str: The answer to the query.
        """
        response = qp.answer(query_str)
        return response

    return FunctionTool.from_defaults(
        fn=answer_query,
        return_direct=True,
        description="A useful tool to answer queries of user about book information.",
    )
