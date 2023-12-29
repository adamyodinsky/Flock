import { string, z } from "zod";

export interface BaseMetaData {
  annotations: { [key: string]: string };
  labels: { [key: string]: string };
  name: string;
  description: string;
}

export interface BaseToolDependency {
  labels: { [key: string]: string };
  name: string;
  kind: "Embedding" | "VectorStore" | "VectorStoreQATool" | "LLM" | "LLMChat" | "LoadTool" | "Splitter" | "Agent" | "PromptTemplate" | "LLMTool" | "EmbeddingsLoader" | "WebScraper" | "CSVTool" | "BrowserTool" | "Custom";
  namespace: string;
  options: Record<string, any>;
  description: string;
}

export interface BaseSpec {
  options: Record<string, any>;
  vendor: string;
  tools: BaseToolDependency[];
  dependencies: BaseToolDependency[];
}

export interface BaseResourceSchema {
  id: string;
  apiVersion: "flock/v1";
  kind: "Embedding" | "VectorStore" | "VectorStoreQATool" | "LLM" | "LLMChat" | "LoadTool" | "Splitter" | "Agent" | "PromptTemplate" | "LLMTool" | "EmbeddingsLoader" | "WebScraper" | "CSVTool" | "BrowserTool" | "Custom";
  category: "other" | "tool" | "scraper" | "model" | "agent" | "deployment" | "job" | "cronjob" | "statefulset";
  namespace: string;
  metadata: BaseMetaData;
  created_at: string;
  updated_at: string;
  spec: BaseSpec;
}


export const BaseToolDependencySchema = z.object({
  labels: z.record(z.string()),
  name: z.string(),
  kind: z.enum([
    'Embedding', 'VectorStore', 'VectorStoreQATool', 'LLM', 'LLMChat', 'LoadTool',
    'Splitter', 'Agent', 'PromptTemplate', 'LLMTool', 'EmbeddingsLoader', 'WebScraper',
    'CSVTool', 'BrowserTool', 'Custom'
  ]),
  namespace: z.string(),
  options: z.record(z.string()),
  description: z.string(),
});

export const resourceFormSchema = z.object({
  name: z.string().max(64),
  description: z.string().max(256),
  namespace: z.string().default("default"),
  kind: string().max(64),
  vendor: string().max(64),
  options: z.array(BaseToolDependencySchema),
  tools: z.array(BaseToolDependencySchema),
});

export const fieldNames = Object.keys(resourceFormSchema.shape);

export type ResourceFormData = z.infer<typeof resourceFormSchema>;

