import { array, string, z } from "zod";


export const resourceFormSchema = z.object({
  name: z.string().max(64),
  description: z.string().max(256),
  namespace: z.string().default("default"),
  kind: string().max(64),
  vendor: string().max(64),
  options: z.record(z.string()),
  dependencies: array(z.object({
    name: string(),
    kind: string(),
    namespace: string()
  })),
  tools: array(z.object({
    name: string(),
    kind: string(),
    namespace: string()
  })),
});

export const fieldNames = Object.keys(resourceFormSchema.shape);

export type ResourceFormData = z.infer<typeof resourceFormSchema>;

