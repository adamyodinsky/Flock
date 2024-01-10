import { string, z } from "zod";
import { Category, Kind, keyValueSchema } from "./general_schemas";


export interface BaseMetaData {
  annotations?: { [key: string]: string };
  labels?: { [key: string]: string };
  name: string;
  description: string;
}


export interface BaseToolDependency {
  labels?: { [key: string]: string };
  name: string;
  kind: Kind;
  namespace: string;
  options?: Record<string, any>;
  // description?: string;
}

export interface OptionsRecord {
  [key: string]: any;
}

export interface BaseSpec {
  vendor: string;
  options?: Record<string, any>;
  tools?: BaseToolDependency[];
  dependencies?: BaseToolDependency[];
}

export interface BaseResourceSchema {
  id?: string;
  apiVersion: "flock/v1";
  kind: string;
  category?: Category;
  namespace: string;
  metadata: BaseMetaData;
  created_at?: string;
  updated_at?: string;
  spec: BaseSpec;
}

export interface ResourceInfoSchema {
  kind: Kind;
  dependencies: Kind[];
  vendor: string[];
}

export const kindValues: ReadonlyArray<string> = Object.values(Kind).map((val) => val as string);
export const kindTuple: [string, ...string[]] = kindValues as [string, ...string[]];


export const baseToolDependencySchema = z.object({
  labels: z.record(z.string()).optional(),
  id: z.string().optional(),
  name: z.string(),
  kind: z.enum(kindTuple),
  namespace: z.string(),
  options: z.record(z.string(), z.any()).optional(),
  description: z.string().optional().nullable(),
});


export const resourceFormSchema = z.object({
  name: z.string().min(3).max(63),
  description: z.string().min(3).max(255),
  namespace: z.string().min(3).max(63).default("default"),
  kind: string().min(3).max(63),
  vendor: string().min(3).max(63),
  options: z.array(keyValueSchema).optional(),
  dependencies: z.array(baseToolDependencySchema).optional(),
  tools: z.array(baseToolDependencySchema).optional(),
});

export const fieldNames = Object.keys(resourceFormSchema.shape);

export type ResourceFormData = z.infer<typeof resourceFormSchema>;



export { Kind };

