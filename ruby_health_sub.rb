 require 'rubygems'
 require 'mqtt'

 client = MQTT::Client.new
 client.host = 'firehose.openstack.org'
 client.port = 1883
 client.connect()
 client.subscribe('ansible/playbook/+/task/health.openstack.org/#')

 client.get do |topic,message|
     puts message
     end
