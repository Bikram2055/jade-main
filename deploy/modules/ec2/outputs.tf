output "server-eip" {
  # list of public ips
  value = aws_eip.server_eip.*.public_ip
}

output "server" {
  value = aws_instance.server.id
}