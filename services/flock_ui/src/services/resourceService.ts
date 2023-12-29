import apiClient from "./apiClient";

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

  private createParams(kind: string = "", name: string = "", namespace: string = "", id: number = 0) {
    let params = {}

    if (id) {
      params = { ...params, id: id }
    }
    if (kind) {
      params = { ...params, kind: kind }
    }
    if (name) {
      params = { ...params, name: name }
    }
    if (namespace) {
      params = { ...params, namespace: namespace }
    }
    return params
  }

  getAll(kind: string = "", name: string = "", namespace: string = "", id: number = 0) {
    const controller = new AbortController();

    const params = this.createParams(
      kind,
      name,
      namespace,
      id
    )

    const request = apiClient
      .get("resources", {
        signal: controller.signal, params: params
      })

    return { request, cancel: () => controller.abort() }
  }

  get(kind: string = "", name: string = "", namespace: string = "", id: number = 0) {

    const params = this.createParams(
      kind,
      name,
      namespace,
      id
    )

    return apiClient
      .get(`resource`, { params: params })
  }
}
