terraform {
  backend "s3" {
    bucket = "System_Monitoring-bucket-for-eks" # Replace with your actual S3 bucket name
    key    = "Jenkins/terraform.tfstate"
    region = "ap-south-1"
  }
}
