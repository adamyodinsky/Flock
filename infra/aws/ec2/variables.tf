variable "tags" {
  type    = map(string)
  default = {}
}

variable "vpc_id" {
  description = "value of the VPC ID"
  type        = string
}

variable "ami" {
  description = "value of the AMI"
  type        = string
}

variable "instance_type" {
  description = "value of the instance type"
  type        = string
}

variable "root_ebs_volume_size" {
  description = "value of the root EBS volume size"
  type        = number
}

variable "data_ebs_volume_size" {
  description = "value of the data EBS volume size"
  type        = number
}

variable "subnet_id" {
  description = "value of the subnet ID"
  type        = string
}

variable "ssh_key_name" {
  description = "value of the SSH key name"
}

variable "ssh_allowed_ips" {
  description = "value of the SSH allowed IP"
  type        = list(string)
}
