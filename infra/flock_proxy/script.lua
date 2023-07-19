local namespace = ngx.var.namespace
local service_name = ngx.var.service

ngx.req.read_body()

-- send the request to the service in the Kubernetes cluster
local res = ngx.location.capture("/proxy_to/" .. service_name .. "." .. namespace .. ".svc.cluster.local", {
  method = ngx.HTTP_POST,
})

-- return the response from the service
ngx.status = res.status
ngx.print(res.body)
