import axios, { CanceledError } from "axios";
import { ConfigKind } from "../deployments_schemas";

const HOST = process.env.DEPLOYER_SERVER_HOST || "localhost";
const PORT = process.env.DEPLOYER_SERVER_PORT || 9900;

const apiClient = axios.create({
  baseURL: `http://${HOST}:${PORT}`,
})

export { CanceledError };


export class ConfigService {
  getAll(kind: ConfigKind = ConfigKind.None) {
    const controller = new AbortController();
    const request = apiClient
      .get("/configs", {
        signal: controller.signal,
        params: { kind: kind }
      })

    return { request, cancel: () => controller.abort() }
  }

  get(kind: string) {
    return apiClient
      .get(`/schema/${kind}`)
  }
}

