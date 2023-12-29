import { string, z } from "zod";

export interface BaseMetaData {
  annotations: { [key: string]: string };
  labels: { [key: string]: string };
  name: string;
  description: string;
}

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


export interface BaseToolDependency {
  labels: { [key: string]: string };
  name: string;
  kind: Kind;
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
  kind: Kind;
  category: Category;
  namespace: string;
  metadata: BaseMetaData;
  created_at: string;
  updated_at: string;
  spec: BaseSpec;
}

export const kindValues: ReadonlyArray<string> = Object.values(Kind).map((val) => val as string);
const kindTuple: [string, ...string[]] = kindValues as [string, ...string[]];


export const baseToolDependencySchema = z.object({
  labels: z.record(z.string()),
  name: z.string(),
  kind: z.enum(kindTuple),
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
  options: z.array(baseToolDependencySchema),
  tools: z.array(baseToolDependencySchema),
});

export const fieldNames = Object.keys(resourceFormSchema.shape);

export type ResourceFormData = z.infer<typeof resourceFormSchema>;

