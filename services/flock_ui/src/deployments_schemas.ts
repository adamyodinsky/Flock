import { z } from "zod";
import { keyValueSchema } from "./general_schemas";

export enum DeploymentKind {
  FlockJob = "FlockJob",
  FlockCronJob = "FlockCronJob",
  FlockDeployment = "FlockDeployment"
}

export const deploymentKindValues: ReadonlyArray<string> = Object.values(DeploymentKind).map((val) => val as string);
const deploymentKindTuple: [string, ...string[]] = deploymentKindValues as [string, ...string[]];

export const deploymentForm = z.object({
  deployment_name: z.string().min(1).max(63),
  deployment_namespace: z.string().default("default"),
  deployment_kind: z.enum(deploymentKindTuple),
  resource_name: z.string().min(1).max(63),
  resource_namespace: z.string().default("default"),
  resource_kind: z.enum(["Agent", "WebScraper"]),
  schedule: z.string(),
  config: z.array(keyValueSchema),
  dry_run: z.boolean(),
});

export type DeploymentFormData = z.infer<typeof deploymentForm>;
