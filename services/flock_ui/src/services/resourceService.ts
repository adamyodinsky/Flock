import apiClient from "./apiClient";

export interface ResourceParams {
  kind?: string;
  name?: string;
  namespace?: string;
  id?: number;
}

export class ResourceSchemaService {
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


export class ResourceService {

  getAll(params: ResourceParams) {
    const controller = new AbortController();

    const request = apiClient
      .get("resources", {
        signal: controller.signal, params: params
      })

    return { request, cancel: () => controller.abort() }
  }

  get(params: ResourceParams) {

    return apiClient
      .get(`resource`, { params: params })
  }
}
