variable "public_subnet_cidrs" {
 type        = list(string)
 description = "Match Service Public Subnet CIDR values"
 default     = ["10.0.0.0/20", "10.0.16.0/20""]
}

variable "private_subnet_cidrs" {
 type        = list(string)
 description = "Match Service Private Subnet CIDR values"
 default     = ["10.0.128.0/20", "10.0.144.0/20"]
}

variable "azs" {
 type        = list(string)
 description = "Availability Zones"
 default     = ["us-east-1a", "us-east-1b"]
}