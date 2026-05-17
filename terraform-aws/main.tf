provider "aws" {
  region = "ap-south-1"
}

resource "aws_security_group" "bugtracker_sg" {
  name = "bugtracker-sg"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "bugtracker_ec2" {
  ami = "ami-0f918f7e67a3323f0"
  instance_type = "t3.micro"
  
  key_name = "bugtracker-keypair"

  security_groups = [
    aws_security_group.bugtracker_sg.name
  ]

  tags = {
    Name = "BugTrackerServer"
  }
}