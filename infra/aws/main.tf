
provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "models" {
  bucket = "terraform-state-bucket-flock"

  tags = {
    Name = "terraform-state-bucket-flock"
  }
}


module "network" {
  source = "./network"
  tags = {
    Group = "Flock"
    App   = "Flock"
  }
}

module "ec2" {
  source               = "./ec2"
  vpc_id               = module.network.vpc_id
  ami                  = var.ami
  subnet_id            = module.network.subnet1_id
  instance_type        = var.instance_type
  root_ebs_volume_size = var.root_ebs_volume_size
  data_ebs_volume_size = var.data_ebs_volume_size
  ssh_key_name         = var.ssh_key_name
  ssh_allowed_ips      = var.ssh_allowed_ips
  tags = {
    Group = "Flock"
    App   = "Flock"
  }
}

