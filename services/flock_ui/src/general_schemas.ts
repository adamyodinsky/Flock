import { z } from "zod";

export const keyValueSchema = z.object({
  key: z.string(),
  value: z.any(),
});

export enum Kind {
  Embedding = "Embedding",
  VectorStore = "VectorStore",
  VectorStoreQATool = "VectorStoreQATool",
  LLM = "LLM",
  LLMChat = "LLMChat",
  LoadTool = "LoadTool",
  Splitter = "Splitter",
  Agent = "Agent",
  PromptTemplate = "PromptTemplate",
  LLMTool = "LLMTool",
  EmbeddingsLoader = "EmbeddingsLoader",
  WebScraper = "WebScraper",
  CSVTool = "CSVTool",
  BrowserTool = "BrowserTool",
  Custom = "Custom",
}

export enum Category {
  Other = "other",
  Tool = "tool",
  Scraper = "scraper",
  Model = "model",
  Agent = "agent",
  Deployment = "deployment",
  Job = "job",
  CronJob = "cronjob",
  StatefulSet = "statefulset",
}

export type KeyValueData = z.infer<typeof keyValueSchema>;
