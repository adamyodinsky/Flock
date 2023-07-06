# /netwrok/main.tf
resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"

  tags = merge({
    Name = "MyVPC"
  }, var.tags)
}

data "aws_region" "current" {}

resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}a"

  tags = merge({
    Name = "MySubnet1"
  }, var.tags)
}

resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}b"

  tags = merge({
    Name = "MySubnet2"
  }, var.tags)
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = merge({
    Name = "MyInternetGateway"
  }, var.tags)
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  tags = merge({
    Name = "MyPublicRouteTable"
  }, var.tags)
}

resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "subnet1" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.public.id
}
