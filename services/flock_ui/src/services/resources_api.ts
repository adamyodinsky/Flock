import axios, { CanceledError } from "axios";
import { BaseResourceSchema } from "../resources_schemas";

const HOST = process.env.RESOURCES_SERVER_HOST || "localhost";
const PORT = process.env.RESOURCES_SERVER_PORT || 80;

const apiClient = axios.create({
  baseURL: `http://${HOST}:${PORT}`,
})

export { CanceledError };


export interface ResourceParams {
  category?: string;
  kind?: string;
  name?: string;
  namespace?: string;
  id?: number;
}

export class ResourceSchemaService {
  getAll() {
    const controller = new AbortController();
    const request = apiClient
      .get("/schemas", {
        signal: controller.signal,
      })

    return { request, cancel: () => controller.abort() }
  }

  get(kind: string) {
    return apiClient
      .get(`/schema/${kind}`)
  }
}


export class ResourceService {

  getAll(params: ResourceParams) {
    const controller = new AbortController();

    const request = apiClient
      .get("/resources", {
        signal: controller.signal, params: params
      })

    return { request, cancel: () => controller.abort() }
  }

  get(params: ResourceParams) {

    return apiClient
      .get("/resource", { params: params })
  }

  post(resource: BaseResourceSchema) {
    return apiClient.post("/resource", resource, {
      headers: {
        'Content-Type': 'application/json',
      }
    })
  }

  delete(id: string) {
    return apiClient.delete(`/resource/${id}`)
  }

  put(resource: BaseResourceSchema) {
    return apiClient.put(`/resource/${resource.id}`, resource)
  }
}

