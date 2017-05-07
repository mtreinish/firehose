package main
import (
  "fmt"
  MQTT "github.com/eclipse/paho.mqtt.golang"
  "os"
  "strconv"
  "time"
)
func onMessageReceived(client MQTT.Client, msg MQTT.Message) {
    fmt.Printf("TOPIC: %s\n", msg.Topic())
    fmt.Printf("MSG: %s\n", msg.Payload())
}
func main() {
    hostname, _ := os.Hostname()
    opts := &MQTT.ClientOptions{
        ClientID: hostname+strconv.Itoa(time.Now().Second()),
    }
    opts.AddBroker("tcp://firehose.openstack.org:1883")
    opts.OnConnect = func(c MQTT.Client) {
        if token := c.Subscribe("ansible/playbook/+/task/health.openstack.org/#", 0, onMessageReceived); token.Wait() && token.Error() != nil {
            fmt.Println(token.Error())
            os.Exit(1)
        }
    }
    client := MQTT.NewClient(opts)
    if token := client.Connect(); token.Wait() && token.Error() != nil {
        panic(token.Error())
    }
    for {
        time.Sleep(1 * time.Second)
    }
}
