
resource "aws_instance" "this" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  key_name      = var.ssh_key_name

  root_block_device {
    volume_size = var.root_ebs_volume_size
  }


  user_data              = data.template_file.this.rendered
  vpc_security_group_ids = [aws_security_group.ssh.id]

  tags = {
    Name = "MyEC2Instance"
  }
}

data "template_file" "this" {
  template = file("${path.module}/user_data.sh")
}

resource "aws_eip" "this" {
  instance = aws_instance.this.id

  tags = {
    Name = "MyElasticIP"
  }
}

resource "aws_security_group" "ssh" {
  name        = "SSH"
  description = "Allow incoming SSH connections"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_allowed_ips
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "data" {
  snapshot_id       = "snap-024681c8a26e785d6"
  availability_zone = aws_instance.this.availability_zone
  size              = var.data_ebs_volume_size
  type              = "gp3"

  tags = {
    Name = "MyEBSDataVolume"
  }
}

resource "aws_volume_attachment" "data" {
  device_name  = "/dev/xvdf"
  volume_id    = aws_ebs_volume.data.id
  instance_id  = aws_instance.this.id
  skip_destroy = true # This allows the volume to be detached without destroying it when the Terraform configuration is destroyed.
}
