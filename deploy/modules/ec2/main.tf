resource "random_shuffle" "subnets" {
  input        = var.subnets
  result_count = 1
}

resource "aws_iam_policy" "ec2_policy" {
  name        = "ec2_policy"
  path        = "/"
  description = "Policy to provide permissions to EC2"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ssm:GetParameters",
          "ssm:GetParameter"
        ],
        Resource = "arn:aws:ssm:us-east-1:${var.account_id}:parameter/jade*"
      }
    ]
  })
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = "RoleForEC2"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "ec2_policy_role" {
  name       = "ec2_policy_attachment"
  roles      = [aws_iam_role.ec2_role.name]
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "server" {
  ami                  = var.instance_ami
  instance_type        = var.instance_size
  user_data            = file("init-script.sh")
  key_name             = "ektaare"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  root_block_device {
    volume_size = var.instance_root_device_size
    volume_type = "gp2"
  }

  subnet_id              = random_shuffle.subnets.result[0]
  vpc_security_group_ids = var.security_groups

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-${var.infra_role}-${terraform.workspace}-server" }
  )
}

resource "aws_eip" "server_eip" {
  # If create eip is true it will create 1 else not
  count = (var.create_eip) ? 1 : 0

  vpc = true

  lifecycle {
    # set true to preserve eip
    prevent_destroy = false
  }

  tags = merge(
    var.common_tags,
    { Name = "${var.prefix}-${var.infra_role}-${terraform.workspace}-server-eip" }
  )
}

resource "aws_eip_association" "server_eip_association" {
  # If create eip is true it will create 1 else not
  count = (var.create_eip) ? 1 : 0

  instance_id = aws_instance.server.id
  # because use of count should get first item
  allocation_id = aws_eip.server_eip[0].id
}