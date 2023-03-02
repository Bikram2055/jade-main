variable "prefix" {
  type        = string
  description = "Prefix for infrastructure"
}

variable "common_tags" {
  type        = map(string)
  description = "Common Tags"
  default     = {}
}

variable "key_pair_name" {
  type        = string
  description = "Key pair name"
  default     = "ektaare"
}

variable "infra_role" {
  type        = string
  description = "Infracture purpose"
}

variable "instance_size" {
  type        = string
  description = "EC2 Server size"
  default     = "t2.small"
}

variable "instance_ami" {
  type        = string
  description = "Server image to use"
}

variable "instance_root_device_size" {
  type        = number
  description = "Root block device size in GB"
  default     = 20
}

variable "subnets" {
  type        = list(string)
  description = "Valid subnets to assign to server"
}

variable "security_groups" {
  type        = list(string)
  description = "Security groups to assign to server"
  default     = []
}

variable "create_eip" {
  type        = bool
  description = "Whether to create Elastic IP or not for instance"
  default     = false
}

variable "account_id" {
  type        = string
  description = "AWS account ID"
}