variable "prefix" {
  type        = string
  description = "Prefix for infrastructure"
}

variable "common_tags" {
  type        = map(string)
  description = "Common Tags"
  default     = {}
}

variable "infra_role" {
  type        = string
  description = "Infracture purpose"
}

variable "vpc_cidr" {
  type        = string
  description = "The IP range to use for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_numbers" {
  type        = map(number)
  description = "Map of AZ to a number that should be used for public subnets"
  default = {
    "us-east-1a" = 1
    "us-east-1b" = 2
    "us-east-1c" = 3
  }
}

variable "private_subnet_numbers" {
  type        = map(number)
  description = "Map of AZ to a number that should be used for private subnets"
  default = {
    "us-east-1a" = 4
    "us-east-1b" = 5
    "us-east-1c" = 6
  }
}

