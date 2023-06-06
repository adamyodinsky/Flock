"""Module for csv processing tool."""

import asyncio
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from flock_schemas import BaseFlockSchema
from flock_schemas.base import Kind
from langchain.agents import tool
from playwright.async_api import async_playwright

from flock_models.resources.base import Resource, ToolResource


class BrowserToolResource(ToolResource):
    """Class for playwright tool."""

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies)

        self.VENDORS = {
            "playwright": self.playwright_browsing,
        }

        if tools is None:
            tools = []

        self.llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(
            Kind.LLMChat
        )

        self.resource = self.VENDORS[self.vendor]

    async def async_load_playwright(self, url: str) -> str:
        """Load the specified URLs using Playwright and parse using BeautifulSoup."""

        results = ""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto(url)

                page_source = await page.content()
                soup = BeautifulSoup(page_source, "html.parser")

                for script in soup(["script", "style"]):
                    script.extract()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (
                    phrase.strip() for line in lines for phrase in line.split("  ")
                )
                results = "\n".join(chunk for chunk in chunks if chunk)
            except Exception as err:
                results = f"Error: {err}"
            await browser.close()
        return results

    def run_async(self, coro):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(coro)

    @tool
    def playwright_browsing(self, url: str) -> str:
        """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
        return self.run_async(self.async_load_playwright(url))
