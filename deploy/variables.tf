variable "prefix" {
  default     = "jade"
  description = "The prefix that should be in the tag name"
}

variable "project" {
  default     = "jade"
  description = "The name of the project"
}

variable "contact" {
  default     = "shishir.subedi@genesesolution.com"
  description = "Contact address"
}

variable "default_region" {
  type        = string
  description = "Default region where your infrastructure is in"
  default     = "us-east-1"
}

variable "default_profile" {
  type        = string
  description = "Default profile to use for credentials"
  default     = "default"
}

variable "web_instance_size" {
  type        = string
  description = "Web Instance size"
  default     = "t2.small"
}

variable "web_instance_root_device_size" {
  type        = number
  description = "Web Instance block storage in GB"
  default     = 20
}

variable "account_id" {
  type        = string
  description = "AWS account ID"
}