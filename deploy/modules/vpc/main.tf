resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-vpc" }
  )
}

resource "aws_subnet" "public" {
  # use count or for_each
  for_each = var.public_subnet_numbers
  vpc_id   = aws_vpc.vpc.id
  # cidrsubnet(prefix, newbits, netnum)
  cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 4, each.value)

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-public-subnet" },
    { Subnet = "${each.key}-${each.value}" }
  )
}

resource "aws_subnet" "private" {
  for_each = var.private_subnet_numbers
  vpc_id   = aws_vpc.vpc.id
  # cidrsubnet(prefix, newbits, netnum)
  cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 4, each.value)

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-private-subnet" },
    { Subnet = "${each.key}-${each.value}" }
  )
}
