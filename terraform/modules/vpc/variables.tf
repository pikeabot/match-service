variable "public_subnet_cidrs" {
 type        = list(string)
 description = "Match Service Public Subnet CIDR values"
 default     = ["10.0.0.0/20", "10.0.16.0/20"]
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

variable "sg_ingress_rules" {
    type = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_block  = string
      description = string
    }))
    default     = [
        {
          from_port   = 443
          to_port     = 443
          protocol    = "tcp"
          cidr_block  = "0.0.0.0/0"
          description = "sqs"
        },
        {
          from_port   = 80
          to_port     = 80
          protocol    = "tcp"
          cidr_block  = "0.0.0.0/0"
          description = "http"
        },
              {
          from_port   = 20
          to_port     = 20
          protocol    = "tcp"
          cidr_block  = "0.0.0.0/0"
          description = "ssh"
        },
    ]
}
