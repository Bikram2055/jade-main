# Public security group
resource "aws_security_group" "public" {
  name        = "${var.prefix}-public-sg"
  description = "Public internet access"
  vpc_id      = aws_vpc.vpc.id

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-public-sg" },
    { VPC = aws_vpc.vpc.id },
    { Role = "Public" }
  )
}

# Rules
resource "aws_security_group_rule" "public_out" {
  # allow all outbound traffic unrestricted
  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.public.id
}

resource "aws_security_group_rule" "public_in_ssh" {
  # allow tcp connection to server from anywhere
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.public.id
}


resource "aws_security_group_rule" "public_in_http" {
  # allow http connection to server from anywhere
  type        = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.public.id
}

resource "aws_security_group_rule" "public_in_https" {
  # allow https connection to server from anywhere
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.public.id
}

# Private security group
resource "aws_security_group" "private" {
  name        = "${var.prefix}-private-sg"
  description = "Private internet access"
  vpc_id      = aws_vpc.vpc.id

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-private-sg" },
    { VPC = aws_vpc.vpc.id },
    { Role = "Private" }
  )
}

# Rules
resource "aws_security_group_rule" "private_out" {
  # allow all outbound traffic unrestricted
  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.private.id
}

resource "aws_security_group_rule" "private_in" {
  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = [aws_vpc.vpc.cidr_block]

  security_group_id = aws_security_group.private.id
}
