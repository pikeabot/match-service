resource "aws_vpc" "match-service-vpc" {
 cidr_block = "10.0.0.0/16"

 tags = {
   Name = "Match Service VPC"
 }
}
resource "aws_subnet" "match-service-public-subnets" {
 count      = length(var.public_subnet_cidrs)
 vpc_id     = aws_vpc.match-service-vpc.id
 cidr_block = element(var.public_subnet_cidrs, count.index)
 availability_zone = element(var.azs, count.index)

 tags = {
   Name = "Match Service Public Subnet ${count.index + 1}"
 }
}

resource "aws_subnet" "match-service-private-subnets" {
 count      = length(var.private_subnet_cidrs)
 vpc_id     = aws_vpc.match-service-vpc.id
 cidr_block = element(var.private_subnet_cidrs, count.index)
 availability_zone = element(var.azs, count.index)

 tags = {
   Name = "Match Service Private Subnet ${count.index + 1}"
 }
}

resource "aws_internet_gateway" "gw" {
 vpc_id = aws_vpc.match-service-vpc.id

 tags = {
   Name = "Match Service IG"
 }
}

resource "aws_route_table" "second_rt" {
 vpc_id = aws_vpc.match-service-vpc.id

 route {
   cidr_block = "0.0.0.0/0"
   gateway_id = aws_internet_gateway.gw.id
 }

 tags = {
   Name = "Match Service 2nd Route Table"
 }
}

resource "aws_route_table_association" "public_subnet_assoc" {
 count = length(var.public_subnet_cidrs)
 subnet_id      = element(aws_subnet.match-service-public-subnets[*].id, count.index)
 route_table_id = aws_route_table.second_rt.id
}

resource "aws_security_group" "match-service-sg" {
  name        = "match-services-sg"
  description = "Allow access to SQS, Lambda and RDS"
  vpc_id      = aws_vpc.match-service-vpc.id

  egress {
   from_port   = 443
   to_port     = 443
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

   tags = {
   Name = "match service sg"
 }
}

resource "aws_security_group_rule" "ingress_rules" {
  count = length(var.sg_ingress_rules)

  type              = "ingress"
  from_port         = var.sg_ingress_rules[count.index].from_port
  to_port           = var.sg_ingress_rules[count.index].to_port
  protocol          = var.sg_ingress_rules[count.index].protocol
  cidr_blocks       = [var.sg_ingress_rules[count.index].cidr_block]
  description       = var.sg_ingress_rules[count.index].description
  security_group_id = aws_security_group.match-service-sg.id
}

