# IGW
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-igw" },
    { VPC = aws_vpc.vpc.id }
  )
}

# NAT gateway (NGW)

# resource "aws_eip" "nat_eip" {
#   vpc = true

#   tags = merge(
#     var.common_tags,
#     { Name = "${var.prefix}-nat-eip" },
#     { VPC = aws_vpc.vpc.id},
#     { Role = "Private"}
#   )
# }

# resource "aws_nat_gateway" "ngw" {
#   allocation_id = aws_eip.nat_eip.id

# # whichever the first public subnet happens to be because NGW needs to be on a public subnnet with an IGW
#   subnet_id = aws_subnet.public[element(keys(aws_subnet.public), 0)].id

#   tags = merge(
#     var.common_tags,
#     { Name = "${var.prefix}-ntw" },
#     { VPC = aws_vpc.vpc.id},
#     { Role = "Private"}
#   )
# }

# Route tables and Route

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-public-rt" },
    { VPC = aws_vpc.vpc.id },
    { Role = "Public" }
  )
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-private-rt" },
    { VPC = aws_vpc.vpc.id },
    { Role = "Private" }
  )
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# resource "aws_route" "private" {
#   route_table_id = aws_route_table.private.id
#   destination_cidr_block = "0.0.0.0/0"
#   nat_gateway_id = aws_nat_gateway.ngw.id
# }

# Route table association

resource "aws_route_table_association" "public" {
  for_each  = aws_subnet.public
  subnet_id = aws_subnet.public[each.key].id

  route_table_id = aws_route_table.public.id
}

# resource "aws_route_table_association" "private" {
#   for_each = aws_subnet.private
#   subnet_id = aws_subnet.private[each.key].id

#   route_table_id = aws_route_table.private.id
# }

