"""Module for csv processing tool."""

from typing import Dict, List, Optional

import pandas as pd
from flock_schemas.base import Kind
from flock_schemas.csv_tool import CSVToolSchema
from langchain.agents import tool
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

from flock_resources.base import Resource, ToolResource


class CSVToolResource(ToolResource):
    """Class for csv processing tool."""

    VENDORS = {}

    def __init__(
        self,
        manifest: CSVToolSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        super().__init__(manifest, dependencies)

        if tools is None:
            tools = []

        self.llm = self.dependencies.get(Kind.LLMChat)

        self.resource = self.process_csv

    @tool
    def process_csv(
        self, csv_file_path: str, instructions: str, output_path: Optional[str] = None
    ) -> str:
        """Process a CSV by with pandas in a limited REPL.\
    Only use this after writing data to disk as a csv file.\
    Any figures must be saved to disk to be viewed by the human.\
    Instructions should be written in natural language, not code. Assume the dataframe is already loaded."""

        try:
            df = pd.read_csv(csv_file_path)
        except Exception as err:
            return f"Error: {err}"
        agent = create_pandas_dataframe_agent(
            self.llm.resource, df, max_iterations=30, verbose=True
        )
        if output_path is not None:
            instructions += f" Save output to disk at {output_path}"
        try:
            result = agent.run(instructions)
            return result
        except Exception as err:
            return f"Error: {err}"


export = {
    "CSVTool": CSVToolResource,
}
