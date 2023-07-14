-- get the namespace and service name from the request
local namespace, service_name = unpack(ngx.var)

-- send the request to the service in the Kubernetes cluster
local res = ngx.location.capture("/proxy_to/" .. namespace .. "." .. service_name .. ".svc.cluster.local")

-- return the response from the service
ngx.status = res.status
ngx.print(res.body)
