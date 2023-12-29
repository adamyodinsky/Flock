import { Kind } from "../schemas";
import { ResourceInfoSchema } from "../schemas";
import apiClient from "./apiClient";

class ResourceSchemaService {
  getAll() {
    const controller = new AbortController();
    const request = apiClient
      .get("schemas", {
        signal: controller.signal,
      })

    return { request, cancel: () => controller.abort() }
  }

  get(kind: Kind) {
    return apiClient
      .get<ResourceInfoSchema>("schema/" + kind)
  }
}

export default new ResourceSchemaService();
