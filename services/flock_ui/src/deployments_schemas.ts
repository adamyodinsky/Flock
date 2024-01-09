import { z } from "zod";
import { keyValueSchema } from "./general_schemas";


const deploymentForm = z.object({
  deployment_name: z.string().min(1).max(63),
  deployment_namespace: z.string().default("default"),
  deployment_kind: z.string(),
  resource_name: z.string().min(1).max(63),
  resource_namespace: z.string().default("default"),
  resource_kind: z.string(),
  schedule: z.string(),
  config: z.array(keyValueSchema),
  dry_run: z.boolean(),
});
