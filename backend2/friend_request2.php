<?php
// PHP libraries for RabbitMQ
require_once __DIR__ . '/../backend1/vendor/autoload.php';
$config = require __DIR__  . '/../messaging/config.php';


use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;


try {
   // Establish RabbitMQ connection
   $rabbitMQConnection = new AMQPStreamConnection(
    $config['rabbitmq']['host'],
    $config['rabbitmq']['port'],
    $config['rabbitmq']['username'],
    $config['rabbitmq']['password']
);
   $channel = $rabbitMQConnection->channel();


   // Declare the queue to listen for MySQL friend request responses
   $channel->queue_declare('mysql_friendrequest_response_queue', false, true, false, false);


   // Declare the queue to send friend request responses to app.py
   $channel->queue_declare('send_friendrequest_response_queue', false, true, false, false);


   // Script waiting for messages
   echo " [*] Waiting for messages from RabbitMQ: mysql_friendrequest_response_queue\n";


   // Callback function to handle incoming RabbitMQ messages
   $callback = function($msg) use ($channel) {
       echo " [x] Received friendrequest response: ", $msg->body, "\n";


       // Holds the success or failure data in a variable
       $friendRequestResponse = $msg->body;


       // Forward the response to send_friendrequest_response_queue
       $message = new AMQPMessage($friendRequestResponse, ['delivery_mode' => 2]); // Make message persistent
       $channel->basic_publish($message, '', 'send_friendrequest_response_queue');
       echo " [x] Sent friend request response to RabbitMQ: send_friendrequest_response_queue\n";
   };


   // Consume messages from the queue: mysql_friendrequest_response_queue
   $channel->basic_consume('mysql_friendrequest_response_queue', '', false, true, false, false, $callback);


   // Keep the script running to listen for incoming messages
   while ($channel->is_consuming()) {
       $channel->wait();
   }


   // Close RabbitMQ connection and channel after processing
   $channel->close();
   $rabbitMQConnection->close();


} catch (Exception $e) {
   echo " [x] RabbitMQ Error: " . $e->getMessage() . "\n";
}
?>



