export const para_stomp = {
    //brokerURL: 'ws://192.168.0.181:15674/ws',
    brokerURL: 'ws://127.0.0.1:15674/ws',
    connectHeaders: {
        login: 'guest',
        passcode: 'guest',
    },
    // // ping pong
    // debug: function (str) {
    //   console.log(str);
    // },
    reconnectDelay: 5000,
    heartbeatIncoming: 4000,
    heartbeatOutgoing: 4000,
}

export const para_stream = {
    'ack': 'client-individual',
    'durable': true,
    'auto-delete': false,
    'x-queue-type': 'stream',
    'prefetch-count': 10,
    'x-stream-offset': 'first'
}
