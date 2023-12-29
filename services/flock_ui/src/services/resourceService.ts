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

  get(kind: string) {
    return apiClient
      .get("schema/" + kind)
  }
}

export default new ResourceSchemaService();
