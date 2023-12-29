import apiClient from "./apiClient";

interface entity {
  id: number
}

class HttpResource<T extends entity> {
  endpoint: string;

  constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  getAll() {
    const controller = new AbortController();
    const request = apiClient
      .get<T[]>(this.endpoint, {
        signal: controller.signal,
      })

    return { request, cancel: () => controller.abort() }
  }

  delete(id: number) {
    return apiClient.delete<T>(this.endpoint + "/" + id)
  }

  create(obj: T) {
    return apiClient
      .post<T>(this.endpoint + "/", obj)
  }

  update(obj: T) {
    return apiClient.patch<T>(this.endpoint + "/" + obj.id, obj)
  }
}

export default HttpService;
