import { z } from "zod";
import { kindTuple } from "./resources_schemas";

export interface ConfigResponseObj {
  id: string
  name: string
  description: string
  kind: string
  target_kind?: string
}

export const SecretKeyRefValueZodSchema = z.object({
  name: z.string(),
  key: z.string(),
});

export const SecretKeyRefZodSchema = z.object({
  secretKeyRef: SecretKeyRefValueZodSchema,
});

export const EnvFromZodSchema = z.object({
  name: z.string(),
  valueFrom: SecretKeyRefZodSchema,
});

export const EnvVarZodSchema = z.object({
  name: z.string(),
  value: z.string(),
});

export const EnvZodSchema = z.union([EnvVarZodSchema, EnvFromZodSchema]);
export type EnvData = z.infer<typeof EnvZodSchema>;

export const DeploymentConfigZodSchema = z.object({
  kind: z.literal("DeploymentConfig"),
  env: z.array(EnvZodSchema),
  image: z.string(),
});
export type DeploymentConfigData = z.infer<typeof DeploymentConfigZodSchema>;

export const DeploymentGlobalConfigZodSchema = DeploymentConfigZodSchema.extend({
  kind: z.literal("DeploymentGlobalConfig"),
});

export const DeploymentKindConfigZodSchema = DeploymentConfigZodSchema.extend({
  kind: z.literal("DeploymentKindConfig"),
  kind_target: z.enum(kindTuple),
});

export enum ConfigKind {
  None = "",
  DeploymentConfig = "DeploymentConfig",
  DeploymentGlobalConfig = "DeploymentGlobalConfig",
  DeploymentKindConfig = "DeploymentKindConfig",
}


// DEPLOYMENT SCHEMAS //

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
  config: DeploymentConfigZodSchema,
  dry_run: z.boolean(),
});

export type DeploymentFormData = z.infer<typeof deploymentForm>;
